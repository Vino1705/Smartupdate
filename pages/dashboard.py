# pages/dashboard.py (Final version with session_state fix)

import streamlit as st
import pandas as pd
import os
import time

CSV_FILE = "logs/decisions.csv"

st.set_page_config(page_title="Smart Update Dashboard", layout="wide")
st.title("🧠 Smart Update Manager Dashboard")

# --- 📡 Real-time Monitoring Controls ---
st.sidebar.header("📡 Real-Time Monitoring")

# Initialize session state for monitoring if it doesn't exist
if "monitoring" not in st.session_state:
    st.session_state.monitoring = False

refresh_rate = st.sidebar.slider("⏱️ Refresh Interval (seconds)", 2, 30, 5)

# Create the button in the sidebar
toggle_button = st.sidebar.button(
    "▶️ Start Monitoring" if not st.session_state.monitoring else "⏸️ Stop Monitoring"
)

# Handle the button click *outside* of the st.sidebar context
if toggle_button:
    st.session_state.monitoring = not st.session_state.monitoring

# --- Check if log file exists ---
if not os.path.exists(CSV_FILE):
    st.warning("⚠️ Log file not found. Run the update agent (main.py) or simulation (simulate_agent.py) first.")
    st.stop()

# --- Load CSV ---
# This part now runs on every refresh
try:
    df = pd.read_csv(CSV_FILE, parse_dates=["timestamp"])
    # Ensure necessary columns are present, fill with default if not (for older logs)
    for col in ["raw_reason", "llm_explanation", "resolution_steps", # NEW: resolution_steps
                "cpu_usage", "battery_level", "user_active", "network", "security_risk_score",
                "current_patch_id", "is_compatible", "compatibility_reason", "patch_size_mb", "patch_reboot_required", "patch_type", "device_id"]: # NEW: device_id
        if col not in df.columns:
            df[col] = "N/A"
    df['action_display'] = df['action'].apply(lambda x: x.replace('_', ' '))
except pd.errors.EmptyDataError:
    st.warning("⚠️ Log file is empty. Run the update agent (main.py) or simulation first to generate data.")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading log file: {e}. Please check '{CSV_FILE}'.")
    st.stop()


# --- Filters ---
st.sidebar.header("🔍 Filters")
action_filter = st.sidebar.multiselect("Select Action", df["action"].unique(), default=df["action"].unique())
device_filter = st.sidebar.multiselect("Select Device", df["device_id"].unique(), default=df["device_id"].unique()) # NEW: device filter
filtered_df = df[df["action"].isin(action_filter) & df["device_id"].isin(device_filter)]

# --- Main Table ---
st.subheader("📋 Recent Update Decisions & Details")
# Display more columns for comprehensive view
display_columns = [
    "timestamp", "device_id", "action_display", "raw_reason", "llm_explanation", "resolution_steps",
    "cpu_usage", "battery_level", "user_active", "network", "security_risk_score",
    "current_patch_id", "patch_type", "patch_size_mb", "patch_reboot_required",
    "is_compatible", "compatibility_reason"
]
# Only show columns that actually exist in the dataframe
display_columns = [col for col in display_columns if col in filtered_df.columns]

st.dataframe(filtered_df.sort_values("timestamp", ascending=False)[display_columns], use_container_width=True)

# --- Charts ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Action Count")
    st.bar_chart(filtered_df["action_display"].value_counts()) # Use action_display for chart

with col2:
    st.subheader("🔋 Battery Levels Over Time")
    if 'timestamp' in filtered_df.columns and 'battery_level' in filtered_df.columns:
        st.line_chart(filtered_df.set_index("timestamp")["battery_level"])

# --- LLM Explanation & Resolution Preview ---
st.subheader("📄 LLM Insights (Preview)")
st.write(filtered_df[["timestamp", "action_display", "llm_explanation", "resolution_steps"]].tail(5))

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