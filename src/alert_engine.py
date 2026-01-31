def detect_risk_acceleration(risk_series, threshold=0.05):
    delta = risk_series.diff()
    if delta.tail(3).mean() > threshold:
        return True, delta.tail(3).mean()
    return False, None
