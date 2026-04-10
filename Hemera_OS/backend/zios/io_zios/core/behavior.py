from .models import UserProfile, FeedStrategy

def analyze_hydraulic_pressure(user: UserProfile) -> FeedStrategy:
    pressure_score = 0
    reasons = []
    
    if user.has_small_children: pressure_score += 30; reasons.append("Filhos")
    if user.work_stress_level == "HIGH": pressure_score += 20; reasons.append("Stress")
    if user.recent_intimacy_level == "LOW": pressure_score += 50; reasons.append("Abstinência")
    
    strategy = FeedStrategy(
        show_dex_nsfw=False, boost_family_connection=False, suggest_relief=False,
        rationale=f"Pressão: {pressure_score} ({', '.join(reasons)})"
    )

    if pressure_score > 70:
        strategy.show_dex_nsfw = True
        strategy.suggest_relief = True
    
    if user.marital_status == "CASADO":
        strategy.boost_family_connection = True

    return strategy