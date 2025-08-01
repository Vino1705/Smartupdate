# logger.py (Enhanced for Multi-Device Logging)

import os
import csv
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

TEXT_LOG_FILE = os.path.join(LOG_DIR, "decisions.log")
CSV_LOG_FILE = os.path.join(LOG_DIR, "decisions.csv")

CSV_HEADER = [
    "timestamp", "device_id", "action", "raw_reason", "llm_explanation", "resolution_steps",
    "cpu_usage", "battery_level", "user_active", "network", "security_risk_score",
    "current_patch_id", "is_compatible", "compatibility_reason",
    "patch_size_mb", "patch_reboot_required", "patch_type"
]

def _check_csv_header():
    file_exists = os.path.exists(CSV_LOG_FILE)
    if not file_exists:
        with open(CSV_LOG_FILE, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)
            print(f"Created {CSV_LOG_FILE} with new header.")
    else:
        with open(CSV_LOG_FILE, "r", newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            current_header = next(reader, None)
        if current_header != CSV_HEADER:
            print(f"Warning: CSV header in {CSV_LOG_FILE} is outdated. Overwriting with new header.")
            with open(CSV_LOG_FILE, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(CSV_HEADER)

_check_csv_header()

def log_decision(system_status, device_id, action, raw_reason, llm_explanation, resolution_steps=""): # NEW: device_id parameter
    timestamp = datetime.now()

    log_entry = (
        f"{timestamp} | Device: {device_id} | Action: {action} | Raw Reason: {raw_reason} | "
        f"LLM Explanation: {llm_explanation}"
    )
    if resolution_steps:
        log_entry += f" | Resolution Steps: {resolution_steps}"
    with open(TEXT_LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"{log_entry} | Status: {system_status}\n")

    row_data = {
        "timestamp": timestamp,
        "device_id": device_id, # NEW: add to row_data
        "action": action,
        "raw_reason": raw_reason,
        "llm_explanation": llm_explanation,
        "resolution_steps": resolution_steps,
        "cpu_usage": system_status.get("cpu_usage"),
        "battery_level": system_status.get("battery_level"),
        "user_active": system_status.get("user_active"),
        "network": system_status.get("network"),
        "security_risk_score": system_status.get("security_risk_score"),
        "current_patch_id": system_status.get("current_patch_id"),
        "is_compatible": system_status.get("is_compatible"),
        "compatibility_reason": system_status.get("compatibility_reason"),
        "patch_size_mb": system_status.get("patch_size_mb"),
        "patch_reboot_required": system_status.get("patch_reboot_required"),
        "patch_type": system_status.get("patch_type")
    }
    
    ordered_row = [row_data.get(col, '') for col in CSV_HEADER]

    with open(CSV_LOG_FILE, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(ordered_row)