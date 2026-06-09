import pytest
import asyncio
import json
import base64
from cryptography.hazmat.primitives.asymmetric import x25519
from fastapi_service.hermes.double_ratchet import DoubleRatchetSession
from fastapi_service.hermes.websocket_pool import HermesConnectionPool
from fastapi_service.hermes.zios_bridge import ZiosBridge

# =====================================================================
# 1. TESTES PARA O DOUBLE RATCHET (CRIPTOGRAFIA DE ESTADO DUAL E2EE)
# =====================================================================

def test_double_ratchet_handshake_and_chat():
    # 1. Preparação das chaves
    shared_key = b"\x01" * 32  # Chave mestra pré-compartilhada (gerada pelo X3DH em produção)
    
    # Bob gera um par de chaves DH estático/inicial
    bob_private_key = x25519.X25519PrivateKey.generate()
    bob_pub_bytes = bob_private_key.public_key().public_bytes_raw()

    # 2. Inicialização das sessões
    alice_session = DoubleRatchetSession.init_alice(shared_key, bob_pub_bytes)
    bob_session = DoubleRatchetSession.init_bob(shared_key, bob_private_key)

    # 3. Alice envia mensagem para Bob
    message1 = b"Ola Bob, esta e uma mensagem ultra secreta do Hermes."
    encrypted_msg1 = alice_session.encrypt(message1)

    # Bob descriptografa a mensagem 1 (ele faz o ratchet DH inicial aqui)
    decrypted_msg1 = bob_session.decrypt(encrypted_msg1)
    assert decrypted_msg1 == message1

    # 4. Bob responde a Alice (ratchet DH atualizado)
    message2 = b"Recebido, Alice. O Hermes esta operando em E2EE de Estado Dual."
    encrypted_msg2 = bob_session.encrypt(message2)

    # Alice descriptografa a mensagem 2
    decrypted_msg2 = alice_session.decrypt(encrypted_msg2)
    assert decrypted_msg2 == message2

    # 5. Alice envia mais uma mensagem
    message3 = b"Confirmado. Conexao estavel."
    encrypted_msg3 = alice_session.encrypt(message3)
    decrypted_msg3 = bob_session.decrypt(encrypted_msg3)
    assert decrypted_msg3 == message3


def test_double_ratchet_out_of_order_messages():
    shared_key = b"\x02" * 32
    bob_private_key = x25519.X25519PrivateKey.generate()
    bob_pub_bytes = bob_private_key.public_key().public_bytes_raw()

    alice_session = DoubleRatchetSession.init_alice(shared_key, bob_pub_bytes)
    bob_session = DoubleRatchetSession.init_bob(shared_key, bob_private_key)

    # Alice gera 3 mensagens consecutivas
    msg1 = alice_session.encrypt(b"Mensagem 1")
    msg2 = alice_session.encrypt(b"Mensagem 2")
    msg3 = alice_session.encrypt(b"Mensagem 3")

    # Simulamos entrega fora de ordem: msg3 chega primeiro
    dec3 = bob_session.decrypt(msg3)
    assert dec3 == b"Mensagem 3"

    # Depois msg2 chega
    dec2 = bob_session.decrypt(msg2)
    assert dec2 == b"Mensagem 2"

    # E finalmente msg1 chega
    dec1 = bob_session.decrypt(msg1)
    assert dec1 == b"Mensagem 1"


# =====================================================================
# 2. TESTES PARA O WEBSOCKET CONNECTION POOL
# =====================================================================

class MockWebSocket:
    def __init__(self):
        self.accepted = False
        self.sent_messages = []
        self.closed = False

    async def accept(self):
        self.accepted = True

    async def send_text(self, text: str):
        if self.closed:
            raise RuntimeError("Socket is closed")
        self.sent_messages.append(text)

    async def close(self):
        self.closed = True


@pytest.mark.asyncio
async def test_websocket_pool_management():
    pool = HermesConnectionPool()
    
    ws1 = MockWebSocket()
    ws2 = MockWebSocket()
    ws3 = MockWebSocket()

    # Testa conexões
    await pool.connect("user_alice", ws1)
    await pool.connect("user_alice", ws2)
    await pool.connect("user_bob", ws3)

    assert pool.get_connection_count() == 3
    assert pool.is_user_online("user_alice") is True
    assert pool.is_user_online("user_bob") is True

    # Testa envio de mensagem pessoal (Alice tem 2 conexões/dispositivos)
    sent = await pool.send_personal_message("Olá Alice", "user_alice")
    assert sent is True
    assert len(ws1.sent_messages) == 1
    assert len(ws2.sent_messages) == 1
    assert ws1.sent_messages[0] == "Olá Alice"

    # Testa broadcast
    await pool.broadcast("Mensagem Global")
    assert len(ws1.sent_messages) == 2
    assert len(ws2.sent_messages) == 2
    assert len(ws3.sent_messages) == 1
    assert ws3.sent_messages[0] == "Mensagem Global"

    # Testa desconexão e limpeza
    await pool.disconnect("user_alice", ws1)
    assert pool.get_connection_count() == 2
    
    # Testa envio com falha de conexão (simula socket quebrado)
    ws2.closed = True  # força erro no send_text
    await pool.send_personal_message("Outra mensagem", "user_alice")
    
    # O socket quebrado ws2 deve ter sido automaticamente limpo do pool
    assert pool.is_user_online("user_alice") is False
    assert pool.get_connection_count() == 1  # Apenas Bob restou


# =====================================================================
# 3. TESTES PARA A BRIDGE ZIOS (CANAL LATERAL COGNITIVO)
# =====================================================================

@pytest.mark.asyncio
async def test_zios_bridge_lateral_processing():
    pool = HermesConnectionPool()
    ws_alice = MockWebSocket()
    await pool.connect("alice_id", ws_alice)

    bridge = ZiosBridge(pool)

    # 1. Verifica identificação de comandos ZIOS
    assert bridge.is_zios_command("/zios analisar dados") is True
    assert bridge.is_zios_command("@zios recomendacao") is True
    assert bridge.is_zios_command("conversa humana normal") is False

    # 2. Testa o processamento do comando ZIOS em background (canal lateral)
    await bridge.handle_message("alice_id", "/zios status da rede")
    
    # Dá um breve tempo para a task em background executar
    await asyncio.sleep(0.1)

    # Verifica se Alice recebeu a resposta via WebSocket de forma assíncrona
    assert len(ws_alice.sent_messages) == 1
    
    response_payload = json.loads(ws_alice.sent_messages[0])
    assert response_payload["sender_id"] == "zios"
    assert response_payload["recipient_id"] == "alice_id"
    assert response_payload["is_control"] is True
    assert "status da rede" in response_payload["content"]
