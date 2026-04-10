class ThalamusFilter:
    """
    Porteiro Soberano: Aplica a lei (hard rules) e a vontade do utilizador.
    """
    async def apply(self, request, candidates, user_profile=None):
        clean_list = []
        
        # Regras de Bloqueio do Utilizador
        b_tags = set(user_profile.get("blacklisted_tags", [])) if user_profile else set()
        b_authors = set(user_profile.get("blacklisted_authors", [])) if user_profile else set()

        for c in candidates:
            # 1. Filtro de Bloqueio (Soberania)
            if c.get("author_id") in b_authors:
                continue
            if any(tag in b_tags for tag in c.get("tags", [])):
                continue
                
            # 2. Filtro Legal (Hard Rules do Sistema)
            illegal = ["cp", "terrorism_action"]
            if any(tag in illegal for tag in c.get("tags", [])):
                continue

            # 3. Filtro de Contexto (YourLife vs Outros)
            if request.context == "STUDY" and c.get("safety") != "safe":
                continue

            clean_list.append(c)
            
        return clean_list