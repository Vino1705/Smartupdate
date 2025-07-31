# main.py

import time
from explain_ai import generate_explanation
from monitor import get_system_status
from decision_engine import decide_update
from updater import apply_update, postpone_update
from logger import log_decision

print("🚀 Smart Update Manager (Batch Simulation) is starting...\n")

for cycle in range(5):  # Simulate 5 update cycles
    print(f"\n🔄 Cycle {cycle + 1}")

    # 1. Get current system status
    system_status = get_system_status()
    print(f"📊 Current Status: {system_status}")

    # 2. Decide what to do
    action, reason = decide_update(system_status)
    print(f"🤖 Decision: {action} | Reason: {reason}")

    # 3. Try to get AI explanation
    try:
        explanation = generate_explanation(system_status, action, reason)
        print(f"🗣️ LLM Explanation: {explanation}")
    except Exception as e:
        explanation = f"⚠️ LLM explanation failed: {e}"
        print(explanation)

    # 4. Log the full decision (system state + action + reason + explanation)
    log_decision(system_status, action, reason, explanation)

    # 5. Apply or postpone update
    if action == "Apply":
        apply_update()
    else:
        postpone_update()

    print("✅ Action complete.")
    print("-" * 60)
    time.sleep(2)
