# main.py (Final Version with Multi-Device Simulation)

import time
import os
import joblib
import pandas as pd
from datetime import datetime

# Import your existing modules
from explain_ai import generate_explanation, generate_resolution_steps
from monitor import get_system_status # UPDATED: now accepts device_profile
from decision_engine import decide_update
from updater import apply_update, postpone_update, apply_mini_patch, defer_large_patch_and_schedule, rollback_update
from logger import log_decision # UPDATED: now accepts device_id
from config import IDLE_THRESHOLD, BATTERY_THRESHOLD, SECURITY_RISK_SCORE
from patch_verifier import get_patch_risk_and_compatibility

# --- Define thresholds for Dynamic Optimization ---
LARGE_PATCH_SIZE_MB = 100
BATTERY_OPTIMAL_THRESHOLD = 50
MINI_PATCH_SIZE_MB = 20

# --- Define Multi-Device Simulation Parameters ---
DEVICE_PROFILES = {
    "device_alpha": "normal",
    "device_beta": "busy",
    "device_gamma": "idle",
}

# --- Load the Predictive Model and Encoders ---
MODEL_DIR = 'models'
MODEL_PATH = os.path.join(MODEL_DIR, 'predictive_model.pkl')
LE_NETWORK_PATH = os.path.join(MODEL_DIR, 'le_network.pkl')
LE_DECISION_PATH = os.path.join(MODEL_DIR, 'le_decision.pkl')
USER_IDLE_PATTERNS_PATH = os.path.join(MODEL_DIR, 'user_idle_patterns.pkl')

predictive_model = None
le_network = None
le_decision = None
PREDICTIVE_MODEL_ENABLED = False

user_idle_patterns = None
USER_BEHAVIOR_ADAPTATION_ENABLED = False

try:
    predictive_model = joblib.load(MODEL_PATH)
    le_network = joblib.load(LE_NETWORK_PATH)
    le_decision = joblib.load(LE_DECISION_PATH)
    print("🧠 Predictive model and encoders loaded successfully.")
    PREDICTIVE_MODEL_ENABLED = True
except FileNotFoundError:
    print(f"⚠️ Warning: Predictive model or encoders not found in '{MODEL_DIR}'. Running with rule-based logic only.")
    print("Hint: Please ensure you have run `python train_predictive_model.py` successfully.")
except Exception as e:
    print(f"❌ Error loading predictive model components: {e}. Falling back to rule-based logic only.")

try:
    user_idle_patterns = joblib.load(USER_IDLE_PATTERNS_PATH)
    print("⏰ User idle patterns loaded successfully.")
    USER_BEHAVIOR_ADAPTATION_ENABLED = True
except FileNotFoundError:
    print(f"⚠️ Warning: User idle patterns not found in '{MODEL_DIR}'. Running without user behavior adaptation.")
    print("Hint: Please ensure you have run `python user_behavior_learner.py` successfully.")
except Exception as e:
    print(f"❌ Error loading user idle patterns: {e}. Running without user behavior adaptation.")
    


print("🚀 Smart Update Manager (Multi-Agent Simulation) is starting...\n")

def run_simulation(duration_minutes=1):
    start_time = time.time()
    log_interval = 5
    last_log_time = time.time()
    
    device_ids = list(DEVICE_PROFILES.keys())

    while (time.time() - start_time) < (duration_minutes * 60):
        current_time_loop = time.time()

        if (current_time_loop - last_log_time) >= log_interval:
            print(f"\n🔄 Simulating Cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # --- Iterate through each device agent ---
            for device_id in device_ids:
                device_profile = DEVICE_PROFILES[device_id]
                print(f"\n--- Processing {device_id} (Profile: {device_profile}) ---")
                
                base_system_status = get_system_status(device_profile=device_profile)
                
                current_patch_id, current_patch_details, derived_security_risk_score, is_compatible, compatibility_reason = \
                    get_patch_risk_and_compatibility(base_system_status)

                system_status = {
                    **base_system_status,
                    "security_risk_score": derived_security_risk_score,
                    "current_patch_id": current_patch_id,
                    "is_compatible": is_compatible,
                    "compatibility_reason": compatibility_reason,
                    "patch_size_mb": current_patch_details.get("size_mb", 0),
                    "patch_reboot_required": current_patch_details.get("requires_reboot", False),
                    "patch_type": current_patch_details.get("type", "unknown")
                }

                print(f"📊 Current Status: {system_status}")
                print(f"📦 Incoming Patch: {current_patch_id} | Security Level: {current_patch_details['criticality_score']} | Vulnerability: {current_patch_details['vulnerability_details']} | Type: {current_patch_details['type']} | Size: {current_patch_details['size_mb']}MB | Reboot Required: {current_patch_details['requires_reboot']}")
                print(f"✅ Compatibility: {is_compatible} | Reason: {compatibility_reason}")

                is_idle_window = False
                if USER_BEHAVIOR_ADAPTATION_ENABLED and user_idle_patterns and user_idle_patterns.get("idle_hours"):
                    current_hour = datetime.now().hour
                    is_idle_window = current_hour in user_idle_patterns["idle_hours"]
                    print(f"⏰ Current hour ({current_hour}) is in idle window: {is_idle_window}")

                final_action = ""
                final_reason = ""
                
                if not is_compatible:
                    final_action = "Postpone"
                    final_reason = f"Patch incompatible: {compatibility_reason}"
                    print(f"🛑 Patch Incompatibility Override: {final_action} | Reason: {final_reason}")
                else:
                    rule_action, rule_reason = decide_update(system_status)
                    
                    if rule_action == "Postpone":
                        final_action = rule_action
                        final_reason = rule_reason
                        print(f"🛑 Rule-based decision: {final_action} | Reason: {final_reason} (Critical rule override)")
                    else:
                        if PREDICTIVE_MODEL_ENABLED:
                            try:
                                input_data = {
                                    'cpu_usage': [system_status['cpu_usage']],
                                    'battery_level': [system_status['battery_level']],
                                    'user_activity_encoded': [int(system_status['user_active'])],
                                    'network_status_encoded': [le_network.transform([system_status['network']])[0]],
                                    'security_risk': [system_status['security_risk_score']]
                                }
                                input_df = pd.DataFrame(input_data)
                                
                                predicted_decision_encoded = predictive_model.predict(input_df)[0]
                                ml_suggestion = le_decision.inverse_transform([predicted_decision_encoded])[0]
                                ml_reason_text = f"ML suggested {ml_suggestion} based on learned patterns."
                                print(f"🧠 ML Suggestion: {ml_suggestion}")

                                final_action = ml_suggestion
                                final_reason = ml_reason_text
                                
                                if system_status["security_risk_score"] >= SECURITY_RISK_SCORE and final_action == "Postpone":
                                    final_action = "Apply"
                                    final_reason = f"High security risk ({current_patch_details['vulnerability_details']}). (Rule-based override for critical update)"
                                    print(f"🚨 Rule-based 'Apply' override due to high security risk.")
                                elif is_idle_window and final_action == "Postpone":
                                    final_action = "Apply"
                                    final_reason = "User idle period detected, proceeding with update."
                                    print(f"⏰ Overriding ML Postpone: User idle period detected, attempting to apply update.")
                                
                                if final_action == "Apply":
                                    if system_status["patch_type"] == "security" and \
                                       system_status["patch_size_mb"] <= MINI_PATCH_SIZE_MB and \
                                       not system_status["patch_reboot_required"]:
                                        final_action = "Apply_Mini_Patch"
                                        final_reason = f"Dynamic Optimization: Applying mini-patch for critical security fix ({current_patch_details['vulnerability_details']})."
                                        print(f"⚡ Dynamic Optimization: {final_reason}")
                                    elif system_status["patch_size_mb"] > LARGE_PATCH_SIZE_MB and \
                                         system_status["battery_level"] < BATTERY_OPTIMAL_THRESHOLD:
                                        
                                        final_action = "Defer_Large_Patch"
                                        final_reason = f"Dynamic Optimization: Large patch ({system_status['patch_size_mb']}MB) and battery ({system_status['battery_level']}%) below optimal. Deferring for better conditions."
                                        print(f"⚙️ Dynamic Optimization: {final_reason}")

                            except Exception as e:
                                print(f"❌ Error during ML prediction or UBA/Dynamic Opt integration: {e}. Falling back to rule-based decision.")
                                final_action = rule_action
                                final_reason = rule_reason
                        else:
                            final_action = rule_action
                            final_reason = rule_reason
                            print("Predictive model not enabled. Using rule-based decision only.")

                print(f"🤖 Final Decision: {final_action} | Reason: {final_reason}")

                explanation = ""
                try:
                    explanation = generate_explanation(system_status, final_action, final_reason)
                    print(f"🗣️ LLM Explanation: {explanation}")
                except Exception as e:
                    explanation = f"⚠️ LLM explanation failed: {e}. (Could not generate detailed explanation.)"
                    print(explanation)

                resolution_steps = ""
                if "Postpone" in final_action or "Defer" in final_action:
                    try:
                        resolution_steps = generate_resolution_steps(final_reason, system_status)
                        print(f"🛠️ Resolution Steps: {resolution_steps}")
                    except Exception as e:
                        resolution_steps = f"⚠️ LLM failed to generate resolution steps: {e}"
                        print(resolution_steps)

                is_successful = True
                if final_action == "Apply":
                    is_successful = apply_update(current_patch_details, system_status)
                elif final_action == "Apply_Mini_Patch":
                    is_successful = apply_mini_patch(current_patch_details, system_status)
                elif final_action == "Defer_Large_Patch":
                    defer_large_patch_and_schedule(current_patch_details, system_status)
                else:
                    postpone_update(reason_detail=final_reason)
                
                if not is_successful:
                    rollback_update(current_patch_details)
                    log_reason = f"Update failed, rolled back. Reason: {final_reason}"
                    log_action = "Rollback"
                    explanation = generate_explanation(system_status, "Rollback", log_reason)
                    resolution_steps = "Investigate update logs and re-attempt update under more stable conditions."
                    print(f"🗣️ LLM Explanation for Rollback: {explanation}")

                log_action = final_action if final_action in ["Apply", "Postpone"] else "Apply" if "Apply" in final_action else "Postpone"
                log_reason = final_reason
                log_decision(system_status, device_id, log_action, log_reason, explanation, resolution_steps) # NEW: pass device_id

                print("✅ Action complete.")
                print("-" * 60)

            last_log_time = current_time_loop
        
        time.sleep(1)

    print("\nSmart Update Manager simulation ended.")


if __name__ == "__main__":
    run_simulation(duration_minutes=720)