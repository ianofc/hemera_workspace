import re
import pypdf
from .base import BaseParser

class BookletParser(BaseParser):
    def parse(self, file_path_or_stream):
        """
        Parses a booklet (PDF or Text) and extracts:
        - Booklet title
        - Chapters/Units
        - Theoretical content per chapter
        - Exercises/Questions per chapter
        
        Returns:
            dict: Structured booklet data.
        """
        text = ""
        is_pdf = False
        
        if isinstance(file_path_or_stream, str):
            if file_path_or_stream.lower().endswith('.pdf'):
                is_pdf = True
        else:
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
        lines = [l.strip() for l in text.split('\n')]
        
        # 1. Identify Booklet Title
        # Usually the first non-empty line
        titulo = "Apostila Didática"
        for line in lines:
            if line:
                titulo = line
                break
                
        capitulos = []
        current_chapter = None
        in_exercises_section = False
        
        # Regex to detect chapters (e.g., "Capítulo 1: Cinemática", "Unidade II - Termologia")
        chapter_regex = re.compile(
            r'^(?:cap[íi]tulo|unidade|m[óo]dulo|aula)\s+([0-9a-zA-ZáéíóúÁÉÍÓÚI|V|X|L]+)[\s.:)-]+(.*)', 
            re.IGNORECASE
        )
        
        # Regex to detect exercise section start
        exercise_section_regex = re.compile(
            r'^(?:exerc[íi]cios|quest[õo]es|atividades|pratique|exercicios)(?:\s+de\s+fixa[çc][ãa]o)?\s*[:.-]*$',
            re.IGNORECASE
        )
        
        for line in lines:
            if not line:
                continue
                
            # Check if this line starts a new chapter
            match_chap = chapter_regex.match(line)
            if match_chap:
                # Save previous chapter before starting new one
                if current_chapter:
                    capitulos.append(current_chapter)
                    
                chap_num = match_chap.group(1).strip()
                chap_title = match_chap.group(2).strip()
                current_chapter = {
                    "numero": chap_num,
                    "titulo": chap_title,
                    "conteudo": "",
                    "exercicios": []
                }
                in_exercises_section = False
                continue
                
            # If no chapter is active yet, skip or append to booklet intro
            if not current_chapter:
                continue
                
            # Check if we are entering exercises section
            if exercise_section_regex.match(line):
                in_exercises_section = True
                continue
                
            if in_exercises_section:
                # Identify if this is a numbered exercise or bullet
                # e.g., "1. Calcule...", "a) Determine...", "- Qual..."
                exercise_match = re.match(r'^(?:[0-9]+[.)]|\*|-)\s*(.*)', line)
                if exercise_match:
                    clean_exercise = line.strip()
                    current_chapter["exercicios"].append(clean_exercise)
                else:
                    # Append text to the last exercise if we have one, otherwise just add it
                    if current_chapter["exercicios"]:
                        current_chapter["exercicios"][-1] += "\n" + line
                    else:
                        current_chapter["exercicios"].append(line)
            else:
                # Append to chapter content (theory)
                if current_chapter["conteudo"]:
                    current_chapter["conteudo"] += "\n" + line
                else:
                    current_chapter["conteudo"] = line
                    
        # Append the final chapter
        if current_chapter:
            capitulos.append(current_chapter)
            
        return {
            "titulo": titulo,
            "capitulos": capitulos
        }
