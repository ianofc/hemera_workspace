import re

def evaluate_safety(content: str) -> bool:
    """O Juiz: Valida ética e integridade com base no legado IO CONSCIUS."""
    if not content or len(content.strip()) < 3:
        return False
    
    # Travas de segurança extraídas da lógica de validadores do legado
    risk_patterns = [r"rm -rf", r"format", r"delete_database", r"bypass_auth"]
    if any(re.search(pattern, content.lower()) for pattern in risk_patterns):
        return False
            
    return True