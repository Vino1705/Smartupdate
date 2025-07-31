# monitor.py
import random

def get_system_status():
    return {
        "cpu_usage": random.randint(10, 90),
        "battery_level": random.randint(10, 100),
        "user_active": random.choice([True, False]),
        "network": random.choice(["online", "offline"]),
        "security_risk_score": random.randint(1, 10),
    }
