# pages/simulate_agent.py (Updated to display Dynamic Patch Stream & CVE Details)

import streamlit as st
import pandas as pd
from datetime import datetime
import os
import joblib

from decision_engine import decide_update
from explain_ai import generate_explanation, generate_resolution_steps
from patch_verifier import get_latest_patch, check_patch_compatibility
from config import IDLE_THRESHOLD, BATTERY_THRESHOLD, SECURITY_RISK_SCORE

LOG_FILE = "logs/decisions.csv"
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
    PREDICTIVE_MODEL_ENABLED = True
    st.sidebar.success("🧠 Predictive model loaded.")
except FileNotFoundError:
    st.sidebar.warning("⚠️ Predictive model not found. ML predictions disabled. Run `train_predictive_model.py`.")
except Exception as e:
    st.sidebar.error(f"❌ Error loading predictive model: {e}")

try:
    user_idle_patterns = joblib.load(USER_IDLE_PATTERNS_PATH)
    USER_BEHAVIOR_ADAPTATION_ENABLED = True
    st.sidebar.success("⏰ User idle patterns loaded.")
except FileNotFoundError:
    st.sidebar.warning("⚠️ User idle patterns not found. User Behavior Adaptation disabled. Run `user_behavior_learner.py`.")
except Exception as e:
    st.sidebar.error(f"❌ Error loading user idle patterns: {e}")


st.set_page_config(page_title="🧪 Agent Simulation", layout="centered")
st.title("🧪 Smart Update Agent Simulation")

st.markdown("Simulate update scenarios and test the Smart Update logic using manual inputs. The agent uses its rule-based logic, predictive AI, user behavior adaptation, and patch compatibility checks.")

st.subheader("🛠️ System Parameters")

col1, col2 = st.columns(2)

with col1:
    battery = st.slider("🔋 Battery Level (%)", 0, 100, 50, key="sim_battery")
    cpu = st.slider("🧠 CPU Usage (%)", 0, 100, 50, key="sim_cpu")
    
with col2:
    internet = st.selectbox("🌐 Internet Connection", ["online", "offline"], key="sim_internet")
    user_active_str = st.selectbox("🖱️ User Active?", ["Yes", "No"], key="sim_user_active")
    simulated_hour = st.slider("Current Hour (for UBA)", 0, 23, datetime.now().hour, key="sim_hour")

user_active_bool = (user_active_str == "Yes")

LARGE_PATCH_SIZE_MB = 100
BATTERY_OPTIMAL_THRESHOLD = 50
MINI_PATCH_SIZE_MB = 20

if st.button("🚀 Simulate Decision"):
    st.subheader("Decision Breakdown:")

    base_system_status = {
        "cpu_usage": cpu,
        "battery_level": battery,
        "user_active": user_active_bool,
        "network": internet,
        "security_risk_score": 5
    }

    st.markdown("#### 📦 Patch Assessment")
    # --- GET LATEST PATCH FROM THE STREAM ---
    current_patch_details = get_latest_patch()
    derived_security_risk_score = current_patch_details["criticality_score"]

    is_compatible, compatibility_reason = check_patch_compatibility(current_patch_details, base_system_status)

    system_status = {
        **base_system_status,
        "security_risk_score": derived_security_risk_score,
        "current_patch_id": current_patch_details["id"],
        "is_compatible": is_compatible,
        "compatibility_reason": compatibility_reason,
        "patch_size_mb": current_patch_details.get("size_mb", 0),
        "patch_reboot_required": current_patch_details.get("requires_reboot", False),
        "patch_type": current_patch_details.get("type", "unknown")
    }

    st.write(f"**Incoming Patch:** `{current_patch_details['id']}` | Security Level: `{current_patch_details['criticality_score']}` | **Vulnerability:** `{current_patch_details['vulnerability_details']}` | **Type:** `{current_patch_details['type']}` | Size: `{current_patch_details['size_mb']}MB` | Reboot Required: `{current_patch_details['requires_reboot']}`")
    st.write(f"**Patch Compatibility:** `{is_compatible}` | Reason: `{compatibility_reason}`")

    is_idle_window = False
    if USER_BEHAVIOR_ADAPTATION_ENABLED and user_idle_patterns and user_idle_patterns.get("idle_hours"):
        is_idle_window = simulated_hour in user_idle_patterns["idle_hours"]
        st.write(f"**Current Hour ({simulated_hour}) is in Learned Idle Window:** `{is_idle_window}`")

    final_action = ""
    final_reason = ""
    
    st.markdown("#### 🤖 Decision Process")

    if not is_compatible:
        final_action = "Postpone"
        final_reason = f"Patch incompatible: {compatibility_reason}"
        st.error(f"🛑 Patch Incompatibility Override: **{final_action}** | Reason: {final_reason}")
    else:
        rule_action, rule_reason = decide_update(system_status)
        
        if rule_action == "Postpone":
            final_action = rule_action
            final_reason = rule_reason
            st.warning(f"🛑 Rule-based decision: **{final_action}** | Reason: {final_reason} (Critical rule override)")
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
                    st.info(f"🧠 ML Suggestion: **{ml_suggestion}**")

                    final_action = ml_suggestion
                    final_reason = ml_reason_text
                    
                    if system_status["security_risk_score"] >= SECURITY_RISK_SCORE and final_action == "Postpone":
                        final_action = "Apply"
                        final_reason = f"High security risk ({current_patch_details['vulnerability_details']}). (Rule-based override for critical update)"
                        st.error(f"🚨 Rule-based 'Apply' override due to high security risk.")
                    elif is_idle_window and final_action == "Postpone":
                        final_action = "Apply"
                        final_reason = "User idle period detected, proceeding with update."
                        st.info(f"⏰ Overriding ML Postpone: User idle period detected, attempting to apply update.")
                    
                    if final_action == "Apply":
                        if system_status["patch_type"] == "security" and \
                           system_status["patch_size_mb"] <= MINI_PATCH_SIZE_MB and \
                           not system_status["patch_reboot_required"]:
                            final_action = "Apply_Mini_Patch"
                            final_reason = f"Dynamic Optimization: Applying mini-patch for critical security fix ({current_patch_details['vulnerability_details']})."
                            st.success(f"⚡ Dynamic Optimization: **{final_action.replace('_', ' ')}** | Reason: {final_reason}")
                        elif system_status["patch_size_mb"] > LARGE_PATCH_SIZE_MB and \
                             system_status["battery_level"] < BATTERY_OPTIMAL_THRESHOLD:
                            
                            final_action = "Defer_Large_Patch"
                            final_reason = f"Dynamic Optimization: Large patch ({system_status['patch_size_mb']}MB) and battery ({system_status['battery_level']}%) below optimal. Deferring for better conditions."
                            st.warning(f"⚙️ Dynamic Optimization: **{final_action.replace('_', ' ')}** | Reason: {final_reason}")

                except Exception as e:
                    st.error(f"❌ Error during ML prediction or UBA/Dynamic Opt integration: {e}. Falling back to rule-based decision.")
                    final_action = rule_action
                    final_reason = rule_reason
            else:
                final_action = rule_action
                final_reason = rule_reason
                st.info("Predictive model not enabled. Using rule-based decision only.")

    st.success(f"**🤖 Final Decision: {final_action.replace('_', ' ')}** | Reason: {final_reason}")

    explanation = ""
    try:
        explanation = generate_explanation(system_status, final_action, final_reason)
        st.markdown("#### 🗣️ LLM Explanation")
        st.code(explanation, language="markdown")
    except Exception as e:
        explanation = f"⚠️ LLM explanation failed: {e}. (Could not generate detailed explanation.)"
        st.markdown("#### 🗣️ LLM Explanation")
        st.code(explanation, language="markdown")

    resolution_steps = ""
    if "Postpone" in final_action or "Defer" in final_action:
        try:
            resolution_steps = generate_resolution_steps(final_reason, system_status)
            st.markdown("#### 🛠️ Suggested Resolution Steps")
            st.code(resolution_steps, language="markdown")
        except Exception as e:
            resolution_steps = f"⚠️ LLM failed to generate resolution steps: {e}"
            st.markdown("#### 🛠️ Suggested Resolution Steps")
            st.code(resolution_steps, language="markdown")

    timestamp = datetime.now()
    log_action = final_action if final_action in ["Apply", "Postpone"] else "Apply" if "Apply" in final_action else "Postpone"
    log_reason = final_reason


    new_row = pd.DataFrame([{
        "timestamp": timestamp,
        "action": log_action,
        "raw_reason": log_reason,
        "llm_explanation": explanation,
        "resolution_steps": resolution_steps,
        "cpu_usage": system_status["cpu_usage"],
        "battery_level": system_status["battery_level"],
        "user_active": system_status["user_active"],
        "network": system_status["network"],
        "security_risk_score": system_status["security_risk_score"],
        "current_patch_id": system_status["current_patch_id"],
        "is_compatible": system_status["is_compatible"],
        "compatibility_reason": system_status["compatibility_reason"],
        "patch_size_mb": system_status["patch_size_mb"],
        "patch_reboot_required": system_status["patch_reboot_required"],
        "patch_type": system_status["patch_type"]
    }])

    if os.path.exists(LOG_FILE):
        existing = pd.read_csv(LOG_FILE, parse_dates=["timestamp"])
        updated = pd.concat([existing, new_row], ignore_index=True)
    else:
        updated = new_row
    
    updated.to_csv(LOG_FILE, index=False)


    st.markdown("---")
    st.markdown("### 📋 Recent Simulations")
    if os.path.exists(LOG_FILE):
        st.dataframe(pd.read_csv(LOG_FILE, parse_dates=["timestamp"]).sort_values("timestamp", ascending=False).head(5), use_container_width=True)