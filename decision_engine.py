# decision_engine.py
from config import IDLE_THRESHOLD, BATTERY_THRESHOLD, SECURITY_RISK_SCORE

def decide_update(system_status):
    if system_status["network"] == "offline":
        return "Postpone", "No internet connection."

    if system_status["security_risk_score"] >= SECURITY_RISK_SCORE:
        return "Apply", "High security risk."

    if system_status["cpu_usage"] < IDLE_THRESHOLD and not system_status["user_active"]:
        if system_status["battery_level"] >= BATTERY_THRESHOLD:
            return "Apply", "System idle and battery sufficient."
        else:
            return "Postpone", "Battery too low."
    else:
        return "Postpone", "System busy or user active."
