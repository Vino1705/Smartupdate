# monitor.py (Enhanced for Multi-Device Simulation)

import random
from datetime import datetime

def get_system_status(device_profile="normal"):
    """
    Generates a more realistic system status based on the hour of the day and device profile.
    
    Args:
        device_profile (str): Can be "normal", "busy", or "idle" to simulate different device usage patterns.
    """
    current_hour = datetime.now().hour
    
    is_work_hours = 9 <= current_hour <= 17

    # --- Adjust user_active weights based on profile ---
    if device_profile == "busy":
        active_weight = 0.9
        idle_weight = 0.1
    elif device_profile == "idle":
        active_weight = 0.1
        idle_weight = 0.9
    else: # "normal"
        if is_work_hours:
            active_weight = 0.8
            idle_weight = 0.2
        else:
            active_weight = 0.1
            idle_weight = 0.9
    
    user_active = random.choices([True, False], weights=[active_weight, idle_weight], k=1)[0]

    # --- Generate CPU Usage (correlated with user activity) ---
    if user_active:
        cpu_usage = random.randint(30, 90)
    else:
        cpu_usage = random.randint(10, 40)

    # --- Generate Battery Level ---
    battery_level = random.randint(10, 100)

    # --- Generate Network Status ---
    network = random.choice(["online", "offline"])

    # --- Generate Security Risk Score ---
    security_risk_score = random.randint(1, 10)
    
    return {
        "cpu_usage": cpu_usage,
        "battery_level": battery_level,
        "user_active": user_active,
        "network": network,
        "security_risk_score": security_risk_score,
    }