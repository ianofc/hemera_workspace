import os
import sys
import django
from decimal import Decimal
from django.utils import timezone

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'niocortex.settings')
django.setup()

from lumenios.pedagogico.models import Turma, Disciplina, Atividade, Nota, Aluno
from core.models import CustomUser

def seed_grades():
    print("🌱 Semeando Notas e Atividades no Gradebook...")
    turma = Turma.objects.filter(nome__icontains="3º Ano").first()
    if not turma:
        print("Turma de teste não encontrada.")
        return
        
    prof = CustomUser.objects.filter(username='prof_claudio').first()
    
    # Criar disciplina se não existir
    disciplina, _ = Disciplina.objects.get_or_create(
        nome="Biologia Avançada",
        turma=turma,
        defaults={'professor': prof}
    )
    
    # Criar atividades
    atv1, _ = Atividade.objects.get_or_create(
        titulo="Trabalho de Genética",
        disciplina=disciplina,
        turma=turma,
        defaults={'descricao': "Pesquisa sobre DNA", 'data_entrega': timezone.now()}
    )
    atv2, _ = Atividade.objects.get_or_create(
        titulo="Prova Bimestral 1",
        disciplina=disciplina,
        turma=turma,
        defaults={'descricao': "Capítulos 1 a 3", 'data_entrega': timezone.now()}
    )
    atv3, _ = Atividade.objects.get_or_create(
        titulo="Relatório Lab",
        disciplina=disciplina,
        turma=turma,
        defaults={'descricao': "Mitose celular", 'data_entrega': timezone.now()}
    )
    
    # Distribuir notas para os alunos da turma
    alunos = turma.aluno_set.all()
    notas_mock = [
        [Decimal('8.5'), Decimal('7.0'), Decimal('9.0')],  # Aluno 0
        [Decimal('6.0'), Decimal('5.5'), Decimal('7.5')],  # Aluno 1
        [Decimal('9.5'), Decimal('10.0'), Decimal('9.0')]  # Aluno 2
    ]
    
    for i, aluno in enumerate(alunos):
        if i < len(notas_mock):
            Nota.objects.get_or_create(aluno=aluno, atividade=atv1, defaults={'valor': notas_mock[i][0]})
            Nota.objects.get_or_create(aluno=aluno, atividade=atv2, defaults={'valor': notas_mock[i][1]})
            Nota.objects.get_or_create(aluno=aluno, atividade=atv3, defaults={'valor': notas_mock[i][2]})

    print("✅ Notas distribuídas com sucesso!")

if __name__ == "__main__":
    seed_grades()
