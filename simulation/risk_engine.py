def calculate_risk(
    crowd_density,
    movement_intensity,
    directional_change,
    temporal_prediction,
    xgboost_score,
    bayesian_probability
):
    """
    Calculate the overall simulated crowd risk.
    """

    risk_score = (
        crowd_density * 0.25
        + movement_intensity * 0.20
        + directional_change * 0.15
        + temporal_prediction * 0.15
        + xgboost_score * 0.15
        + bayesian_probability * 0.10
    )

    risk_score = max(0, min(100, risk_score))

    if risk_score < 30:
        risk_level = "LOW"

    elif risk_score < 50:
        risk_level = "MEDIUM"

    elif risk_score < 75:
        risk_level = "HIGH"

    else:
        risk_level = "CRITICAL"

    emergency = risk_level == "CRITICAL"

    return {
        "risk_score": round(risk_score, 2),
        "risk_level": risk_level,
        "emergency": emergency
    }