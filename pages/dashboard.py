# pages/dashboard.py

import streamlit as st
import pandas as pd
import os
import time

CSV_FILE = "logs/decisions.csv"

st.set_page_config(page_title="Smart Update Dashboard", layout="wide")
st.title("🧠 Smart Update Manager Dashboard")

# --- 📡 Real-time Monitoring Controls ---
st.sidebar.header("📡 Real-Time Monitoring")

if "monitoring" not in st.session_state:
    st.session_state.monitoring = False

refresh_rate = st.sidebar.slider("⏱️ Refresh Interval (seconds)", 2, 30, 5)

toggle = st.sidebar.button(
    "▶️ Start Monitoring" if not st.session_state.monitoring else "⏸️ Stop Monitoring"
)

if toggle:
    st.session_state.monitoring = not st.session_state.monitoring

# --- Check if log file exists ---
if not os.path.exists(CSV_FILE):
    st.warning("⚠️ Log file not found. Run the update agent first.")
    st.stop()

# --- Load CSV ---
df = pd.read_csv(CSV_FILE, parse_dates=["timestamp"])

# --- Filters ---
st.sidebar.header("🔍 Filters")
action_filter = st.sidebar.multiselect("Select Action", df["action"].unique(), default=df["action"].unique())
filtered_df = df[df["action"].isin(action_filter)]

# --- Main Table ---
st.subheader("📋 Recent Update Decisions")
st.dataframe(filtered_df.sort_values("timestamp", ascending=False), use_container_width=True)

# --- Charts ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Action Count")
    st.bar_chart(filtered_df["action"].value_counts())

with col2:
    st.subheader("🔋 Battery Levels")
    st.line_chart(filtered_df[["timestamp", "battery_level"]].set_index("timestamp"))

# --- LLM Explanation Preview ---
st.subheader("📄 LLM Explanations (Preview)")
st.write(filtered_df[["timestamp", "action", "explanation"]].tail(5))

# --- Download Button ---
csv_download = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("📥 Download CSV Log", csv_download, "smart_update_log.csv", "text/csv")

# --- 🔁 Rerun Only After Rendering ---
if st.session_state.monitoring:
    st.sidebar.success("✅ Monitoring enabled...")
    time.sleep(refresh_rate)
    st.rerun()

else:
    st.sidebar.warning("⏸️ Monitoring paused.")
