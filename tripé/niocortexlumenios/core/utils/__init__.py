
import random
import string
import unicodedata

def gerar_matricula_zios():
    "Gera uma matrícula aleatória"
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(10))

def gerar_email_institucional(nome, sobrenome):
    "Gera email padrão: nome.sobrenome@niocortex.edu"
    def remove_accents(input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    
    clean_nome = remove_accents(nome.lower().split()[0])
    clean_sobrenome = remove_accents(sobrenome.lower().split()[-1])
    return f"{clean_nome}.{clean_sobrenome}@niocortex.edu"
