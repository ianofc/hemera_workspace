import logging
import re
from typing import Any, Dict, List, Optional

logger = logging.getLogger("TALAMUS_INGRESS")


class TalamusIngress:
    def __init__(self):
        # Regras legais de veto absoluto
        self.illegal_terms = ["cp", "terrorism_action", "terrorism", "hate_speech_extreme"]

    def sanitize_string(self, text: str) -> str:
        """
        Remove tags HTML, scripts e normaliza espaços para evitar injeções
        """
        if not text:
            return ""
        
        # 1. Remove tags HTML (prevenção de XSS)
        clean = re.sub(r"<[^>]*>", "", text)
        
        # 2. Remove caracteres de controle / ASCII invisíveis potencialmente maliciosos
        clean = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", clean)
        
        # 3. Escapa aspas simples e limpa caracteres SQL perigosos
        clean = clean.replace("'", "''").replace(";", "")
        
        return clean.strip()

    def sanitize_tags(self, tags: List[str]) -> List[str]:
        """
        Sanitiza a lista de tags e remove termos ilegais ou vazios
        """
        if not tags:
            return []
        
        clean_tags = []
        for tag in tags:
            if not tag:
                continue
            sanitized = self.sanitize_string(str(tag)).lower().strip()
            
            # Filtro Legal: Se a tag for ilegal, não a inclui ou veta a inclusão
            if sanitized in self.illegal_terms:
                logger.warning(f"🚫 [TALAMUS VETO] Tag proibida detectada e vetada: {sanitized}")
                continue
            
            if sanitized:
                clean_tags.append(sanitized)
                
        return clean_tags

    def sanitize_event_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitiza todos os campos de texto do payload do evento de entrada
        """
        if not payload:
            return {}

        sanitized = {}
        for key, val in payload.items():
            if isinstance(val, str):
                sanitized[key] = self.sanitize_string(val)
            elif isinstance(val, list):
                if key == "tags":
                    sanitized[key] = self.sanitize_tags(val)
                else:
                    sanitized[key] = [self.sanitize_string(str(item)) if isinstance(item, str) else item for item in val]
            elif isinstance(val, dict):
                sanitized[key] = self.sanitize_event_payload(val)
            else:
                sanitized[key] = val
                
        return sanitized

    def validate_recommend_request(self, user_id: str, context: str) -> bool:
        """
        Valida parâmetros básicos do request do gateway
        """
        if not user_id or not isinstance(user_id, str):
            return False
        
        # Validação do user_id contra ataques de injeção direta no ID
        clean_user_id = self.sanitize_string(user_id)
        if clean_user_id != user_id:
            return False
            
        return True


thalamus_ingress = TalamusIngress()
