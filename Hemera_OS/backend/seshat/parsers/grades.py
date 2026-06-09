import re
from decimal import Decimal
import pypdf
from .base import BaseParser

class GradesParser(BaseParser):
    def parse(self, file_path_or_stream):
        """
        Parses a grades PDF and extracts:
        - Class/Turma name
        - Headers of activities
        - List of students with their respective grades and situation
        
        Returns:
            dict: {
                "turma_nome_original": str,
                "atividades": list of str,
                "alunos": list of dict {
                    "nome": str,
                    "notas": list of Decimal,
                    "situacao": str
                }
            }
        """
        reader = pypdf.PdfReader(file_path_or_stream)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        if not lines:
            raise ValueError("No readable text found in the PDF.")
            
        # 1. Identify Turma Name
        turma_nome_original = None
        # Try to find class name in the first few lines
        for line in lines[:5]:
            match_turma = re.search(r'TURMA\s+(.+?)\s+\-', line, re.IGNORECASE)
            if match_turma:
                turma_nome_original = match_turma.group(1).strip()
                break
        
        if not turma_nome_original:
            # Fallback regex search in the entire text
            match_turma = re.search(r'TURMA\s+(.+?)\s+\-', text, re.IGNORECASE)
            if match_turma:
                turma_nome_original = match_turma.group(1).strip()
            else:
                turma_nome_original = "Turma Nao Identificada"

        # 2. Identify header for Activities
        idx_aluno = -1
        idx_situacao = -1
        for i, l in enumerate(lines):
            if l.upper() == "ALUNO":
                idx_aluno = i
            elif l.upper() in ["SITUAÇÃO", "SITUACAO"]:
                idx_situacao = i
                break
                
        if idx_aluno == -1 or idx_situacao == -1:
            raise ValueError("Invalid PDF format. Could not locate 'ALUNO' and 'SITUAÇÃO' headers.")
            
        header_names = lines[idx_aluno+1 : idx_situacao] 
        # Clean up TOTAL from headers
        if "TOTAL" in header_names:
            header_names.remove("TOTAL")
        if "Total" in header_names:
            header_names.remove("Total")
            
        atividades = [h for h in header_names if h not in ["ALUNO", "SITUAÇÃO", "SITUACAO"]]
        
        # 3. Parse Students and Grades
        data_lines = lines[idx_situacao+1:]
        alunos = []
        i = 0
        
        # Grade matching pattern: matches digits with optional comma/dot and decimals
        grade_pattern = re.compile(r'^[0-9]+([.,][0-9]+)?$')
        
        # Clean list of strings that represent page headers/footers to skip
        noise_words = {
            "ALUNO", "SITUAÇÃO", "SITUACAO", "RELATÓRIO DE NOTAS", "TOTAL",
            "1ª UNIDADE", "2ª UNIDADE", "3ª UNIDADE", "4ª UNIDADE",
            "1O BIMESTRE", "2O BIMESTRE", "3O BIMESTRE", "4O BIMESTRE"
        }
        
        while i < len(data_lines):
            line_val = data_lines[i]
            
            # Skip noise or headers repeated across pages
            if (line_val.upper() in noise_words or 
                "TURMA" in line_val.upper() or 
                line_val.startswith("-")):
                i += 1
                continue
                
            nome_aluno = line_val
            
            # Skip invalid short names or page numbers
            if len(nome_aluno) < 3 or nome_aluno.isdigit():
                i += 1
                continue
                
            # The next lines should contain grades, followed by total and situation
            i += 1
            notas_extraidas = []
            
            # Gather all consecutive lines matching grades pattern
            while i < len(data_lines) and grade_pattern.match(data_lines[i]):
                val = data_lines[i].replace(',', '.')
                notas_extraidas.append(Decimal(val))
                i += 1
                
            # Check for situation (APROVADO, REPROVADO, etc.)
            situacao = "Frequente"  # Default
            if i < len(data_lines) and data_lines[i].upper() in [
                "APROVADO", "REPROVADO", "RECUPERAÇÃO", "RECUPERACAO", 
                "EXAME FINAL", "DESISTENTE", "TRANSFERIDO"
            ]:
                situacao = data_lines[i]
                i += 1
                
            # If we extracted student details, save them
            alunos.append({
                "nome": nome_aluno,
                "notas": notas_extraidas,
                "situacao": situacao
            })
            
        return {
            "turma_nome_original": turma_nome_original,
            "atividades": atividades,
            "alunos": alunos
        }
