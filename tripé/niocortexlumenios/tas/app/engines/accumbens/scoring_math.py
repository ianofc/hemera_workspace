class DopamineWeights:
    CLICK = 1.0
    LIKE = 3.0
    COMMENT = 6.0
    SHARE = 12.0  # Maior recompensa para o motor
    BOREDOM_PENALTY = -5.0 # Penalidade para conteúdo repetido