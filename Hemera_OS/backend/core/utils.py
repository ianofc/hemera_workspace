# core/utils.py
import datetime
import random
import re
from django.utils.text import slugify

def gerar_matricula_zios():
    """
    Gera matrícula no formato: AAAAMMRRRSSSS
    Ex: 202501884102
    """
    agora = datetime.datetime.now()
    aaaa = agora.year
    mm = f"{agora.month:02d}"
    rr = f"{random.randint(10, 99)}" # 2 dígitos aleatórios
    ssss = f"{random.randint(1000, 9999)}" # 4 dígitos sequenciais/aleatórios do lote
    
    return f"{aaaa}{mm}{rr}{ssss}"

def gerar_email_institucional(nome_completo, instituicao_slug="niocortex"):
    """
    Gera email: nome_sobrenome@instituicao.niocortex.com
    Respeita nomes compostos (First Name).
    Ex: Ana Julia Silva -> ana_julia_silva
    """
    # Limpa espaços extras
    partes = nome_completo.strip().split()
    
    if not partes:
        return f"usuario_{random.randint(1000,9999)}@{instituicao_slug}.niocortex.com"
        
    # Lógica para identificar nome composto vs sobrenome
    # Simplificação: Tudo exceto o último é "nome", o último é "sobrenome"
    # Para o email, vamos concatenar tudo com underline
    
    slug_nome = slugify(nome_completo).replace('-', '_')
    return f"{slug_nome}@{instituicao_slug}.niocortex.com"