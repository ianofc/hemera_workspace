import base64
from typing import Dict, Tuple, Optional
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from pydantic import BaseModel

def kdf_rk(rk: bytes, dh_out: bytes) -> Tuple[bytes, bytes]:
    """
    Key Derivation Function para a Root Key.
    Deriva uma nova Root Key e Chain Key usando HKDF-SHA256.
    """
    hkdf = HKDF(
        algorithm=SHA256(),
        length=64,
        salt=b'\x00' * 32,
        info=b'HermesRootRatchet',
        backend=None
    )
    okm = hkdf.derive(rk + dh_out)
    return okm[0:32], okm[32:64]

def kdf_ck(ck: bytes) -> Tuple[bytes, bytes]:
    """
    Key Derivation Function para a Chain Key.
    Deriva a próxima Chain Key e a Message Key usando HMAC-SHA256.
    """
    h_msg = HMAC(ck, SHA256())
    h_msg.update(b'\x01')
    message_key = h_msg.finalize()

    h_chain = HMAC(ck, SHA256())
    h_chain.update(b'\x02')
    next_chain_key = h_chain.finalize()

    return next_chain_key, message_key

class MessageHeader(BaseModel):
    dh_pub: str  # Chave pública DH do remetente codificada em base64
    pn: int      # Número de mensagens da cadeia anterior
    n: int       # Número de sequência nesta cadeia

class EncryptedMessage(BaseModel):
    header: MessageHeader
    ciphertext: str  # Texto cifrado codificado em base64
    nonce: str       # Nonce de 12 bytes codificado em base64

class DoubleRatchetSession:
    def __init__(self, shared_key: bytes):
        """
        Inicializa uma sessão Double Ratchet usando uma chave compartilhada mestre inicial (32 bytes).
        """
        self.rk: bytes = shared_key
        self.dhs: x25519.X25519PrivateKey = x25519.X25519PrivateKey.generate()
        self.dhr: Optional[x25519.X25519PublicKey] = None
        self.cks: Optional[bytes] = None
        self.ckr: Optional[bytes] = None
        self.ns: int = 0
        self.nr: int = 0
        self.pn: int = 0
        # Armazena chaves de mensagens puladas: mapeia (dhr_public_bytes, sequence_number) -> message_key
        self.mkskipped: Dict[Tuple[bytes, int], bytes] = {}

    @classmethod
    def init_alice(cls, shared_key: bytes, bob_dh_pub_bytes: bytes) -> "DoubleRatchetSession":
        """
        Inicializa a sessão do lado da Alice.
        Alice inicia a conversa e conhece a chave pública do Bob.
        """
        session = cls(shared_key)
        session.dhr = x25519.X25519PublicKey.from_public_bytes(bob_dh_pub_bytes)
        
        # Deriva a primeira chave de envio
        dh_out = session.dhs.exchange(session.dhr)
        session.rk, session.cks = kdf_rk(session.rk, dh_out)
        return session

    @classmethod
    def init_bob(cls, shared_key: bytes, bob_private_key: x25519.X25519PrivateKey) -> "DoubleRatchetSession":
        """
        Inicializa a sessão do lado do Bob.
        Bob usa sua chave privada existente para responder à Alice.
        """
        session = cls(shared_key)
        session.dhs = bob_private_key
        # Bob não conhece a chave DH da Alice até receber a primeira mensagem.
        return session

    def encrypt(self, plaintext: bytes, ad: bytes = b"") -> EncryptedMessage:
        """
        Criptografa o plaintext usando a chave da cadeia de envio atual.
        """
        if self.cks is None:
            # Se a cadeia de envio não estiver inicializada (caso de Bob no início, antes de Alice mandar msg)
            raise ValueError("Cadeia de envio não inicializada.")

        # Deriva a Message Key
        self.cks, mk = kdf_ck(self.cks)
        
        # Prepara o cabeçalho
        dh_pub_bytes = self.dhs.public_key().public_bytes_raw()
        header = MessageHeader(
            dh_pub=base64.b64encode(dh_pub_bytes).decode('utf-8'),
            pn=self.pn,
            n=self.ns
        )
        self.ns += 1

        # Criptografa usando AES-GCM
        nonce = AESGCM.generate_nonce()
        aesgcm = AESGCM(mk)
        
        # O cabeçalho serializado em JSON serve como Associated Data (AD)
        header_json = header.model_dump_json().encode('utf-8')
        combined_ad = header_json + ad
        
        ciphertext_bytes = aesgcm.encrypt(nonce, plaintext, combined_ad)

        return EncryptedMessage(
            header=header,
            ciphertext=base64.b64encode(ciphertext_bytes).decode('utf-8'),
            nonce=base64.b64encode(nonce).decode('utf-8')
        )

    def decrypt(self, msg: EncryptedMessage, ad: bytes = b"") -> bytes:
        """
        Decodifica e descriptografa a mensagem criptografada.
        Trata mensagens fora de ordem e atualizações de ratchet DH.
        """
        header = msg.header
        dh_pub_bytes = base64.b64decode(header.dh_pub.encode('utf-8'))
        ciphertext_bytes = base64.b64decode(msg.ciphertext.encode('utf-8'))
        nonce_bytes = base64.b64decode(msg.nonce.encode('utf-8'))
        
        header_json = header.model_dump_json().encode('utf-8')
        combined_ad = header_json + ad

        # 1. Verifica se a chave desta mensagem já foi pulada e armazenada
        if (dh_pub_bytes, header.n) in self.mkskipped:
            mk = self.mkskipped.pop((dh_pub_bytes, header.n))
            aesgcm = AESGCM(mk)
            return aesgcm.decrypt(nonce_bytes, ciphertext_bytes, combined_ad)

        # 2. Se a chave pública DH recebida for nova, faz o ratchet de recebimento/DH
        if self.dhr is None or dh_pub_bytes != self.dhr.public_bytes_raw():
            self.skip_message_keys(header.pn)
            self.dh_ratchet(header)

        # 3. Pula quaisquer mensagens perdidas na cadeia atual
        self.skip_message_keys(header.n)

        # 4. Deriva a Message Key atual
        self.ckr, mk = kdf_ck(self.ckr)
        self.nr += 1

        # 5. Decripta a mensagem
        aesgcm = AESGCM(mk)
        return aesgcm.decrypt(nonce_bytes, ciphertext_bytes, combined_ad)

    def dh_ratchet(self, header: MessageHeader):
        """
        Realiza a atualização do ratchet DH.
        """
        self.pn = self.ns
        self.ns = 0
        self.nr = 0
        
        dh_pub_bytes = base64.b64decode(header.dh_pub.encode('utf-8'))
        self.dhr = x25519.X25519PublicKey.from_public_bytes(dh_pub_bytes)

        # Deriva a chave de recebimento
        dh_out_recv = self.dhs.exchange(self.dhr)
        self.rk, self.ckr = kdf_rk(self.rk, dh_out_recv)

        # Gera novo par de chaves próprio para envio
        self.dhs = x25519.X25519PrivateKey.generate()

        # Deriva a chave de envio
        dh_out_send = self.dhs.exchange(self.dhr)
        self.rk, self.cks = kdf_rk(self.rk, dh_out_send)

    def skip_message_keys(self, until: int):
        """
        Salva chaves de mensagens que foram puladas (por exemplo, devido a pacotes fora de ordem).
        """
        if self.ckr is not None:
            # Limite razoável de segurança para evitar loop infinito
            if self.nr + 2000 < until:
                raise ValueError("Muitas mensagens puladas, possível ataque ou dessincronização.")
            
            while self.nr < until:
                self.ckr, mk = kdf_ck(self.ckr)
                dhr_bytes = self.dhr.public_bytes_raw() if self.dhr else b""
                self.mkskipped[(dhr_bytes, self.nr)] = mk
                self.nr += 1
