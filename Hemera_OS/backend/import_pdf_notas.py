import os
import sys
import re
from decimal import Decimal
from django.utils import timezone

# Setting up django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')

import django
django.setup()

import PyPDF2
from core.models import CustomUser, School
from lumenios.pedagogico.models import Turma, Aluno, Disciplina, Atividade, Nota

def get_or_create_school():
    # Garantir que exista uma Escola default
    school, _ = School.objects.get_or_create(
        nome="Hemera Escola Padrão"
    )
    return school

def extract_notas():
    notas_dir = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'NOTAS'))
    if not os.path.exists(notas_dir):
        print(f"DIRETORIO {notas_dir} NAO ENCONTRADO.")
        return
        
    school = get_or_create_school()
    
    # Criar um professor padrao (O Ian)
    prof_ian, created = CustomUser.objects.get_or_create(
        email="ianworktech@gmail.com",
        defaults={
            "username": "ian_santos",
            "first_name": "Ian",
            "last_name": "Santos",
            "role": "Teacher",
            "school": school
        }
    )
    if created:
        prof_ian.set_password("134679")
        prof_ian.save()

    arquivos = [f for f in os.listdir(notas_dir) if f.endswith('.pdf')]
    print(f"🔎 Encontrados {len(arquivos)} PDFs de Notas.")
    
    for file in arquivos:
        path = os.path.join(notas_dir, file)
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if not lines: continue
        
        # A primeira linha costuma ter a Turma "TURMA 1ª A ADM - RELATÓRIO DE NOTAS"
        header = lines[0]
        match_turma = re.search(r'TURMA\s+(.+?)\s+\-', header)
        if not match_turma:
            continue
            
        turma_nome_antiga = match_turma.group(1).strip()
        
        # Aplicar regra de transição temporal
        turma_nome_nova = turma_nome_antiga
        if "3ª" in turma_nome_antiga or "3º" in turma_nome_antiga:
            print(f"⏩ Turma {turma_nome_antiga} ignorada (Alunos formados).")
            continue
        elif "2ª" in turma_nome_antiga or "2º" in turma_nome_antiga:
            turma_nome_nova = turma_nome_antiga.replace("2ª", "3ª").replace("2º", "3º")
        elif "1ª" in turma_nome_antiga or "1º" in turma_nome_antiga:
            turma_nome_nova = turma_nome_antiga.replace("1ª", "2ª").replace("1º", "2º")
            
        print(f"🏫 Criando/Atualizando Turma de {turma_nome_antiga} PARA -> {turma_nome_nova}")
        
        turma, _ = Turma.objects.get_or_create(
            nome=turma_nome_nova,
            defaults={
                "ano_letivo": 2026,
                "professor_regente": prof_ian
            }
        )
        
        # Criar disciplina para atrelar as atividades
        disciplina, _ = Disciplina.objects.get_or_create(
            nome="Disciplina Base", turma=turma, professor=prof_ian
        )
        
        # Encontrar os Headers para criar as Atividades
        # Ex: ['ALUNO', 'PROVA 17/11', 'TRAB 25/11', ...]
        idx_aluno = -1
        idx_situacao = -1
        for i, l in enumerate(lines):
            if l == "ALUNO":
                idx_aluno = i
            elif l == "SITUAÇÃO" or l == "SITUACAO":
                idx_situacao = i
                break
                
        if idx_aluno == -1 or idx_situacao == -1:
            print("Formato não reconhecido.")
            continue
            
        header_names = lines[idx_aluno+1 : idx_situacao] 
        # O último normalmente é TOTAL
        if "TOTAL" in header_names:
            header_names.remove("TOTAL")
            
        atividades = []
        for h in header_names:
            ativ, _ = Atividade.objects.get_or_create(
                turma=turma,
                disciplina=disciplina,
                titulo=h,
                defaults={"descricao": f"Importado do PDF: {h}", "data_entrega": timezone.now()}
            )
            atividades.append(ativ)
            
        data_lines = lines[idx_situacao+1:]
        
        # Parse dos alunos
        # O formato intercala: Nome, Nota1, Nota2..., Total, Situação
        i = 0
        while i < len(data_lines):
            # O nome do aluno pode vir puro ou se for pagina nova ter "SITUAÇÃO" aleatoria (vou pular sujeira)
            if data_lines[i] in ["ALUNO", "SITUAÇÃO", "3ª Unidade", "RELATÓRIO DE NOTAS"] or "TURMA" in data_lines[i]:
                i += 1
                continue
                
            nome_aluno = data_lines[i]
            
            # As próximas N linhas são números (notas)
            i += 1
            notas_extraidas = []
            while i < len(data_lines) and re.match(r'^[0-9]+,[0-9]+$', data_lines[i]):
                notas_extraidas.append(data_lines[i])
                i += 1
            
            # Pula TOTAL (se houver) e SITUAÇÃO
            if i < len(data_lines) and data_lines[i] in ["APROVADO", "REPROVADO", "RECUPERAÇÃO", "EXAME FINAL"]:
                i += 1
                
            # Verifica se não é titulo perdidos ou páginas (ex: "1")
            if len(nome_aluno) < 3 or nome_aluno.isdigit():
                continue
                
            # Extração limpa, vamos criar o Aluno
            email_base = nome_aluno.split()[0].lower() + "." + (nome_aluno.split()[-1].lower() if len(nome_aluno.split())>1 else "aluno")
            email = f"{email_base}@hemera.io"
            
            user, created = CustomUser.objects.get_or_create(
                username=email_base,
                defaults={
                    "first_name": nome_aluno.split()[0],
                    "last_name": " ".join(nome_aluno.split()[1:]),
                    "email": email,
                    "role": "Student",
                    "school": school
                }
            )
            if created:
                user.set_password("aluno123")
                user.save()
                
            aluno, created = Aluno.objects.get_or_create(
                usuario=user,
                defaults={
                    "matricula": "26" + str(user.id).zfill(4)
                }
            )
            # Associar a turma
            aluno.turma = turma
            aluno.save()
            
            # Associar Notas
            for j in range(min(len(notas_extraidas), len(atividades))):
                valor_float = Decimal(notas_extraidas[j].replace(',', '.'))
                Nota.objects.update_or_create(
                    aluno=aluno,
                    atividade=atividades[j],
                    defaults={"valor": valor_float}
                )
                
    print("🚀 MIGRAÇÃO CONCLUÍDA! Alunos transferidos no tempo :)")

if __name__ == "__main__":
    extract_notas()
