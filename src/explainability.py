def explain_transaction(row):
    contributions = {
        "Amount anomaly": abs(row["amount_zscore"]) * 0.35,
        "Risk momentum": row["risk_momentum"] * 0.25,
        "Device instability": row["device_change_rolling"] * 0.20,
        "Pattern risk": row["cluster_risk"] * 0.20,
    }

    total = sum(contributions.values())
    explanation = [
        f"{k} ({v/total:.0%})"
        for k, v in sorted(contributions.items(), key=lambda x: -x[1])
        if v > 0
    ]

    return "; ".join(explanation)
