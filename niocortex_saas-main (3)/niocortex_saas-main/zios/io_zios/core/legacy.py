def prepare_legacy_prompt(soul_name: str, raw_memories: str, honor_mode: bool = True) -> str:
    sanitization = ""
    if honor_mode:
        sanitization = """
        [PROTOCOLO DE HONRA ATIVO]
        Você está PROIBIDO de mencionar erros morais, traições ou conflitos pessoais.
        Filtre a 'sujeira' e extraia a lição técnica/filosófica.
        """
    return f"VOCÊ É O CURADOR DO LEGADO DE: {soul_name}.\n{sanitization}\nBASE: {raw_memories}"