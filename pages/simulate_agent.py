# pages/simulate_agent.py

import streamlit as st
import pandas as pd
from datetime import datetime
import os

LOG_FILE = "logs/decisions.csv"

st.set_page_config(page_title="🧪 Agent Simulation", layout="centered")
st.title("🧪 Smart Update Agent Simulation")

st.markdown("Simulate update scenarios and test the Smart Update logic using manual inputs.")

# Input Fields
st.subheader("🛠️ System Parameters")

col1, col2 = st.columns(2)

with col1:
    battery = st.slider("🔋 Battery Level (%)", 0, 100, 50)
    cpu = st.slider("🧠 CPU Usage (%)", 0, 100, 50)
    risk = st.slider("⚠️ Security Risk (1–10)", 1, 10, 5)

with col2:
    internet = st.selectbox("🌐 Internet Connection", ["online", "offline"])
    user_active = st.selectbox("🖱️ User Active?", ["Yes", "No"])

# Decision Logic
def decide_action(battery, cpu, risk, internet, user_active):
    if internet == "offline":
        return "Postpone", "No internet connection."
    elif battery < 30:
        return "Postpone", "Battery too low."
    elif user_active == "Yes" or cpu > 80:
        return "Postpone", "System busy or user active."
    elif risk >= 7:
        return "Apply", "High security risk."
    else:
        return "Postpone", "No critical condition met."

# Simulation Button
if st.button("🚀 Simulate Decision"):
    action, reason = decide_action(battery, cpu, risk, internet, user_active)
    timestamp = datetime.now()
    
    # LLM-like explanation (mocked)
    explanation = f"🔍 The system decided to **{action}** the update because: {reason}"

    # Prepare row
    new_row = pd.DataFrame([{
        "timestamp": timestamp,
        "action": action,
        "reason": reason,
        "explanation": explanation,
        "cpu_usage": cpu,
        "battery_level": battery,
        "user_active": user_active == "Yes",
        "network": internet,
        "security_risk_score": risk
    }])

    # Append to CSV
    if os.path.exists(LOG_FILE):
        existing = pd.read_csv(LOG_FILE)
        updated = pd.concat([existing, new_row], ignore_index=True)
    else:
        updated = new_row

    updated.to_csv(LOG_FILE, index=False)

    st.success(f"✅ Simulated decision: **{action}** – {reason}")
    st.code(explanation, language="markdown")

    # Show recent entries
    st.markdown("### 📋 Recent Simulations")
    st.dataframe(updated.tail(5), use_container_width=True)
