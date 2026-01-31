def ensemble_risk(rule_score, ml_score):
    return 0.6 * rule_score + 0.4 * ml_score
