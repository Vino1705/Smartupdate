# start_app.py
import subprocess
import time

print("Starting Smart Update Agent...")
# Use Popen to run the process in the background
agent_process = subprocess.Popen(['python', 'main.py'])

# Give it a moment to start
time.sleep(5)

print("Starting Streamlit Dashboard...")
# Launch the dashboard in the foreground
subprocess.run(['streamlit', 'run', 'pages/dashboard.py'])