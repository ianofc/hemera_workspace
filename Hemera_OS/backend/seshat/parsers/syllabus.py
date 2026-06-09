import re
import pypdf
from .base import BaseParser

class SyllabusParser(BaseParser):
    def parse(self, file_path_or_stream):
        """
        Parses a syllabus document (PDF or Text) and extracts:
        - Disciplina (Subject)
        - Carga Horária (Hours)
        - Objetivos (Objectives)
        - Habilidades (BNCC Skills / Competencies)
        - Conteúdo Programático (Structured Topics/Modules)
        - Referências / Bibliografia (References)
        
        Returns:
            dict: Structured syllabus data.
        """
        text = ""
        # Check if the input is a PDF (by inspecting bytes or file path)
        is_pdf = False
        
        if isinstance(file_path_or_stream, str):
            if file_path_or_stream.lower().endswith('.pdf'):
                is_pdf = True
        else:
            # File-like object, check starting bytes
            try:
                current_pos = file_path_or_stream.tell()
                header = file_path_or_stream.read(4)
                file_path_or_stream.seek(current_pos)
                if header == b'%PDF':
                    is_pdf = True
            except (AttributeError, IOError):
                pass
                
        if is_pdf:
            reader = pypdf.PdfReader(file_path_or_stream)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        else:
            if isinstance(file_path_or_stream, str):
                with open(file_path_or_stream, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            else:
                text = file_path_or_stream.read()
                if isinstance(text, bytes):
                    text = text.decode('utf-8', errors='ignore')
                    
        return self._parse_text(text)
        
    def _parse_text(self, text):
        # 1. Subject/Disciplina
        disciplina = "Disciplina Não Identificada"
        match_disc = re.search(r'(?i)(?:disciplina|componente\s+curricular|curso)[:\s]+([^\n]+)', text)
        if match_disc:
            disciplina = match_disc.group(1).strip()
            
        # 2. Carga Horária
        carga_horaria = ""
        match_ch = re.search(r'(?i)(?:carga\s+hor[áa]ria|c\.h\.|horas)[:\s]+([^\n]+)', text)
        if match_ch:
            carga_horaria = match_ch.group(1).strip()
            
        # 3. Objetivos
        objetivos = ""
        match_obj = re.search(
            r'(?i)(?:objetivos?|objetivo\s+geral)[:\s]+(.*?)(?=\n\s*(?:habilidades|compet[êe]ncias|bncc|conte[úu]do|cronograma|refer[êe]ncias|bibliografia|$))', 
            text, 
            re.DOTALL
        )
        if match_obj:
            objetivos = match_obj.group(1).strip()
            
        # 4. Habilidades / BNCC
        habilidades = ""
        match_hab = re.search(
            r'(?i)(?:habilidades|compet[êe]ncias|bncc)[:\s]+(.*?)(?=\n\s*(?:objetivos?|conte[úu]do|cronograma|refer[êe]ncias|bibliografia|$))', 
            text, 
            re.DOTALL
        )
        if match_hab:
            habilidades = match_hab.group(1).strip()
            
        # 5. Referências
        referencias = ""
        match_ref = re.search(
            r'(?i)(?:refer[êe]ncias|bibliografia|leituras)[:\s]+(.*?)(?=\n\s*(?:objetivos?|habilidades|compet[êe]ncias|conte[úu]do|cronograma|$))', 
            text, 
            re.DOTALL
        )
        if match_ref:
            referencias = match_ref.group(1).strip()
            
        # 6. Conteúdo Programático
        conteudo_raw = ""
        match_cont = re.search(
            r'(?i)(?:conte[úu]do\s+program[áa]tico|programa\s+da\s+disciplina|t[óo]picos|conte[úu]do)[:\s]+(.*?)(?=\n\s*(?:refer[êe]ncias|bibliografia|objetivos?|habilidades|compet[êe]ncias|$))', 
            text, 
            re.DOTALL
        )
        if match_cont:
            conteudo_raw = match_cont.group(1).strip()
        else:
            # Fallback if no specific section heading, look for any lines starting with numbers/topics
            conteudo_raw = ""
            
        # Parse topics/modules from conteudo_raw
        conteudo_programatico = []
        if conteudo_raw:
            # Look for lines starting with numbers, letters, Roman numerals, or dash/bullet
            # Ex: "1. Introdução", "Módulo I: Vetores", "Tópico A -"
            lines = [l.strip() for l in conteudo_raw.split('\n') if l.strip()]
            order = 1
            for line in lines:
                # Check if it looks like a heading or new topic
                match_topic = re.match(r'^(?:(?:m[óo]dulo|unidade|cap[íi]tulo)\s+)?([0-9a-zA-ZáéíóúÁÉÍÓÚI|V|X|L]+)[\s.:)-]+(.*)', line, re.IGNORECASE)
                if match_topic:
                    num = match_topic.group(1).strip()
                    title = match_topic.group(2).strip()
                    conteudo_programatico.append({
                        "titulo": f"{num}. {title}" if num else title,
                        "ordem": order,
                        "detalhes": ""
                    })
                    order += 1
                elif line.startswith('-') or line.startswith('*'):
                    # Bullet point under the last topic
                    clean_line = line.lstrip('-* ').strip()
                    if conteudo_programatico:
                        last_topic = conteudo_programatico[-1]
                        if last_topic["detalhes"]:
                            last_topic["detalhes"] += "; " + clean_line
                        else:
                            last_topic["detalhes"] = clean_line
                    else:
                        conteudo_programatico.append({
                            "titulo": clean_line,
                            "ordem": order,
                            "detalhes": ""
                        })
                        order += 1
                else:
                    # Append as details to the last topic, or create new topic
                    if conteudo_programatico:
                        last_topic = conteudo_programatico[-1]
                        if last_topic["detalhes"]:
                            last_topic["detalhes"] += "\n" + line
                        else:
                            last_topic["detalhes"] = line
                    else:
                        conteudo_programatico.append({
                            "titulo": line,
                            "ordem": order,
                            "detalhes": ""
                        })
                        order += 1
                        
        return {
            "disciplina": disciplina,
            "carga_horaria": carga_horaria,
            "objetivos": objetivos,
            "habilidades": habilidades,
            "conteudo_programatico": conteudo_programatico,
            "referencias": referencias
        }
