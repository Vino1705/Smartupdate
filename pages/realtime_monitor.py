# pages/realtime_monitor.py
"""
import streamlit as st
import pandas as pd
import os

CSV_FILE = "logs/decisions.csv"

st.set_page_config(page_title="📡 Real-Time Monitor", layout="wide")
st.title("📡 Smart Update Real-Time Monitor")

# Auto-refresh every 5 seconds
st.markdown("<meta http-equiv='refresh' content='5'>", unsafe_allow_html=True)

# Check if CSV exists
if not os.path.exists(CSV_FILE):
    st.warning("⚠️ Log file not found. Please run the update agent or simulation.")
    st.stop()

# Load data
df = pd.read_csv(CSV_FILE, parse_dates=["timestamp"])
latest = df.sort_values("timestamp", ascending=False).iloc[0]

# 📡 Snapshot
st.subheader("📸 Latest System Snapshot")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("🕒 Time", latest["timestamp"].strftime("%H:%M:%S"))
col2.metric("🔋 Battery", f'{latest["battery_level"]}%')
col3.metric("🧠 CPU", f'{latest["cpu_usage"]}%')
col4.metric("🌐 Network", latest["network"])
col5.metric("🖱️ User Active", "Yes" if latest["user_active"] else "No")

# 🔔 Warnings
if latest["battery_level"] < 20:
    st.error("🔴 Battery is critically low!")
if latest["cpu_usage"] > 90:
    st.warning("🟠 CPU usage is very high!")
if latest["security_risk_score"] >= 7:
    st.warning("⚠️ High security risk detected!")

# 💬 Explanation
st.subheader("💬 Last Decision Explanation")
st.info(f"**{latest['action']}** – {latest['reason']}\n\n{latest['explanation']}")
"""
