# logger.py
import os
import csv
from datetime import datetime

# Ensure log directories exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# File paths
TEXT_LOG_FILE = os.path.join(LOG_DIR, "decisions.log")
CSV_LOG_FILE = os.path.join(LOG_DIR, "decisions.csv")

# Write CSV header only once (if file doesn't exist)
if not os.path.exists(CSV_LOG_FILE):
    with open(CSV_LOG_FILE, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp", "action", "raw_reason", "llm_explanation",
            "cpu_usage", "battery_level", "user_active", "network", "security_risk_score"
        ])

def log_decision(system_status, action, raw_reason, llm_explanation):
    timestamp = datetime.now()

    # 1️⃣ Text Log (Developer Friendly)
    with open(TEXT_LOG_FILE, "a", encoding="utf-8") as log:
        log.write(
            f"{timestamp} | Action: {action} | Raw Reason: {raw_reason} | "
            f"LLM Explanation: {llm_explanation} | Status: {system_status}\n"
        )

    # 2️⃣ CSV Log (Data Friendly)
    with open(CSV_LOG_FILE, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            timestamp,
            action,
            raw_reason,
            llm_explanation,
            system_status["cpu_usage"],
            system_status["battery_level"],
            system_status["user_active"],
            system_status["network"],
            system_status["security_risk_score"]
        ])
