import re
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from core.models import School
from lumenios.pedagogico.models import Turma, Aluno, Disciplina, Atividade, Nota, PlanoDeAula

CustomUser = get_user_model()

class SeshatIndexer:
    def __init__(self, school_name="Hemera Escola Padrão", default_teacher_email="ianworktech@gmail.com"):
        self.school_name = school_name
        self.default_teacher_email = default_teacher_email

    def _get_or_create_school(self):
        school, _ = School.objects.get_or_create(
            nome=self.school_name
        )
        return school

    def _get_or_create_default_teacher(self, school):
        teacher, created = CustomUser.objects.get_or_create(
            email=self.default_teacher_email,
            defaults={
                "username": "ian_santos",
                "first_name": "Ian",
                "last_name": "Santos",
                "role": "Teacher",
                "school": school,
                "is_professor": True
            }
        )
        if created:
            teacher.set_password("134679")
            teacher.save()
        return teacher

    def _apply_temporal_transition(self, turma_nome_antiga):
        """
        Applies transition rules:
        - 3ª / 3º class: Ignored (students graduated)
        - 2ª / 2º class: Becomes 3ª / 3º
        - 1ª / 1º class: Becomes 2ª / 2º
        """
        if not turma_nome_antiga:
            return None
            
        if "3ª" in turma_nome_antiga or "3º" in turma_nome_antiga:
            return None
            
        turma_nome_nova = turma_nome_antiga
        if "2ª" in turma_nome_antiga:
            turma_nome_nova = turma_nome_antiga.replace("2ª", "3ª")
        elif "2º" in turma_nome_antiga:
            turma_nome_nova = turma_nome_antiga.replace("2º", "3º")
        elif "1ª" in turma_nome_antiga:
            turma_nome_nova = turma_nome_antiga.replace("1ª", "2ª")
        elif "1º" in turma_nome_antiga:
            turma_nome_nova = turma_nome_antiga.replace("1º", "2º")
            
        return turma_nome_nova

    @transaction.atomic
    def index_grades(self, parsed_grades, apply_transition=True, teacher=None):
        """
        Indexes parsed grades data into the Django database.
        
        Args:
            parsed_grades (dict): Output from GradesParser.parse.
            apply_transition (bool): If True, applies class promotion rules.
            teacher (CustomUser, optional): Teacher to assign. If None, uses default.
            
        Returns:
            dict: Summary of indexing operations (created classes, students, grades, etc.).
        """
        school = self._get_or_create_school()
        if not teacher:
            teacher = self._get_or_create_default_teacher(school)
            
        original_turma_nome = parsed_grades["turma_nome_original"]
        
        if apply_transition:
            turma_nome = self._apply_temporal_transition(original_turma_nome)
            if not turma_nome:
                return {
                    "status": "ignored",
                    "reason": f"Turma {original_turma_nome} has graduated."
                }
        else:
            turma_nome = original_turma_nome
            
        # Create Turma
        turma, turma_created = Turma.objects.get_or_create(
            nome=turma_nome,
            defaults={
                "ano_letivo": 2026,
                "professor": teacher
            }
        )
        
        # Create Disciplina Base
        disciplina, disc_created = Disciplina.objects.get_or_create(
            nome="Disciplina Base",
            turma=turma,
            defaults={
                "professor": teacher
            }
        )
        
        # Create Atividades
        atividades_db = []
        for ativ_titulo in parsed_grades["atividades"]:
            ativ, _ = Atividade.objects.get_or_create(
                turma=turma,
                disciplina=disciplina,
                titulo=ativ_titulo,
                defaults={
                    "professor": teacher,
                    "descricao": f"Importada do PDF: {ativ_titulo}",
                    "data_entrega": timezone.now().date(),
                    "valor_maximo": Decimal("10.0")
                }
            )
            atividades_db.append(ativ)
            
        students_indexed = 0
        grades_indexed = 0
        
        for student_data in parsed_grades["alunos"]:
            nome = student_data["nome"]
            notas = student_data["notas"]
            situacao = student_data["situacao"]
            
            # Generate student credentials
            name_parts = nome.split()
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
            
            email_prefix = first_name.lower() + "." + (name_parts[-1].lower() if len(name_parts) > 1 else "aluno")
            email = f"{email_prefix}@hemera.io"
            
            # Use get_or_create for student CustomUser
            student_user, user_created = CustomUser.objects.get_or_create(
                username=email_prefix,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "role": "Student",
                    "school": school,
                    "is_aluno": True
                }
            )
            if user_created:
                student_user.set_password("aluno123")
                student_user.save()
                
            # Create Aluno profile
            aluno, aluno_created = Aluno.objects.get_or_create(
                usuario=student_user,
                defaults={
                    "nome": nome,
                    "matricula": "26" + str(student_user.id.hex[:6]).upper(),
                    "email": email,
                    "turma": turma,
                    "professor": teacher
                }
            )
            
            # Make sure student is in the current class/turma
            if aluno.turma != turma:
                aluno.turma = turma
                aluno.save()
                
            students_indexed += 1
            
            # Link grades
            for j in range(min(len(notas), len(atividades_db))):
                Nota.objects.update_or_create(
                    aluno=aluno,
                    atividade=atividades_db[j],
                    defaults={
                        "valor": notas[j],
                        "feedback": f"Situação original: {situacao}"
                    }
                )
                grades_indexed += 1
                
        return {
            "status": "indexed",
            "turma": turma_nome,
            "turma_created": turma_created,
            "disciplina": disciplina.nome,
            "atividades_criadas": len(atividades_db),
            "alunos_indexados": students_indexed,
            "notas_indexadas": grades_indexed
        }

    @transaction.atomic
    def index_syllabus(self, parsed_syllabus, turma_obj=None, teacher=None):
        """
        Indexes parsed syllabus data into Disciplina and Planos de Aula.
        
        Args:
            parsed_syllabus (dict): Output from SyllabusParser.parse.
            turma_obj (Turma, optional): Turma to link. If None, creates a default one.
            teacher (CustomUser, optional): Teacher to assign. If None, uses default.
            
        Returns:
            dict: Summary of indexing operations.
        """
        school = self._get_or_create_school()
        if not teacher:
            teacher = self._get_or_create_default_teacher(school)
            
        if not turma_obj:
            turma_obj, _ = Turma.objects.get_or_create(
                nome="Turma Geral SESHAT",
                defaults={
                    "ano_letivo": 2026,
                    "professor": teacher
                }
            )
            
        disciplina_nome = parsed_syllabus["disciplina"]
        disciplina, _ = Disciplina.objects.get_or_create(
            nome=disciplina_nome,
            turma=turma_obj,
            defaults={
                "professor": teacher
            }
        )
        
        planos_criados = 0
        
        # Each topic in the syllabus content becomes a PlanoDeAula
        for topic in parsed_syllabus["conteudo_programatico"]:
            PlanoDeAula.objects.create(
                turma=turma_obj,
                professor=teacher,
                titulo=topic["titulo"],
                conteudo=topic["detalhes"] or "Conteúdo detalhado na ementa.",
                habilidades_bncc=parsed_syllabus["habilidades"] or None,
                objetivos=parsed_syllabus["objetivos"] or None,
                referencias=parsed_syllabus["referencias"] or None,
                data_prevista=timezone.now().date(),
                status='Planejado'
            )
            planos_criados += 1
            
        return {
            "status": "indexed",
            "disciplina": disciplina_nome,
            "turma": turma_obj.nome,
            "planos_de_aula_criados": planos_criados
        }

    @transaction.atomic
    def index_booklet(self, parsed_booklet, disciplina_obj=None, teacher=None):
        """
        Indexes parsed booklet data. Creates PlanoDeAula objects representing booklet chapters.
        
        Args:
            parsed_booklet (dict): Output from BookletParser.parse.
            disciplina_obj (Disciplina, optional): Disciplina to associate. If None, creates/uses default.
            teacher (CustomUser, optional): Teacher to assign. If None, uses default.
            
        Returns:
            dict: Summary of indexing operations.
        """
        school = self._get_or_create_school()
        if not teacher:
            teacher = self._get_or_create_default_teacher(school)
            
        if not disciplina_obj:
            turma_obj, _ = Turma.objects.get_or_create(
                nome="Turma Geral SESHAT",
                defaults={
                    "ano_letivo": 2026,
                    "professor": teacher
                }
            )
            disciplina_obj, _ = Disciplina.objects.get_or_create(
                nome=parsed_booklet["titulo"],
                turma=turma_obj,
                defaults={
                    "professor": teacher
                }
            )
            
        planos_criados = 0
        atividades_criadas = 0
        
        for chap in parsed_booklet["capitulos"]:
            title = f"Capítulo {chap['numero']}: {chap['titulo']}"
            
            # Create a PlanoDeAula for the chapter
            plano = PlanoDeAula.objects.create(
                turma=disciplina_obj.turma,
                professor=teacher,
                titulo=title,
                conteudo=chap["conteudo"],
                data_prevista=timezone.now().date(),
                status='Planejado'
            )
            planos_criados += 1
            
            # If the chapter has exercises, create a corresponding Atividade
            if chap["exercicios"]:
                exercises_text = "\n".join(chap["exercicios"])
                Atividade.objects.create(
                    turma=disciplina_obj.turma,
                    disciplina=disciplina_obj,
                    professor=teacher,
                    titulo=f"Exercícios - {title}",
                    descricao=f"Resolver os seguintes exercícios da apostila:\n\n{exercises_text}",
                    data_entrega=timezone.now().date(),
                    valor_maximo=Decimal("10.0")
                )
                atividades_criadas += 1
                
        return {
            "status": "indexed",
            "apostila_titulo": parsed_booklet["titulo"],
            "planos_de_aula_criados": planos_criados,
            "atividades_de_exercicio_criadas": atividades_criadas
        }
