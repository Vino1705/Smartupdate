## 🧠 Smart Update Manager with Agentic AI
An intelligent, multi-layered agent for autonomous and safe device updates,
designed for critical environments like healthcare.
## Project Overview
This project tackles the critical problem of managing software and firmware updates
on smart devices, particularly in sensitive contexts like healthcare. Traditional update
systems are often rigid, risky, and unexplainable, potentially leading to dangerous
interruptions or security vulnerabilities.
Our solution is a comprehensive, Agentic AI–powered system that autonomously
decides, explains, and executes update actions based on a deep understanding of
real-time device conditions, user behavior, and patch-specific risks.
## Key Features
This prototype demonstrates a complete, end-to-end intelligent update pipeline,
including:
● Autonomous Decision Engine: A central orchestrator that makes intelligent
choices (Apply, Postpone, Rollback) by combining multiple AI layers.
● Layered Intelligence: A decision hierarchy that prioritizes safety rules first, then
consults a predictive ML model, and finally adapts to user behavior and dynamic
conditions.
● Predictive Analytics: A machine learning model, trained on historical data, to
predict the most optimal time for an update.
● User Behavior Adaptation: The system learns and adapts to individual device
usage patterns, identifying "idle windows" to avoid interruptions.
● Patch Risk & Compatibility Assessment: A dynamic verifier that simulates
assessing patches for security criticality (CVEs) and compatibility with the
device's resources.
● Dynamic Optimization: The agent can choose nuanced actions beyond simple
Apply/Postpone, such as applying small "mini-patches" for urgent fixes or
deferring large updates when conditions are not optimal.
● Resilience & Rollback Simulation: The system is designed to handle failures. It
can simulate an update failure and automatically initiate a rollback to a stable
state, logging the event for analysis.
● Explainable AI: Uses a lightweight LLM (gpt2) to generate human-readable
explanations for every decision and provides actionable resolution steps for
postponed or failed updates.
● Multi-Agent Simulation: The system is designed to simulate a fleet of devices
(agents), each with its own profile, showcasing the solution's scalability.
● Interactive UI & Real-time Dashboard: A Streamlit application provides a
powerful interface to manually simulate scenarios and a real-time dashboard to
monitor the actions of all simulated agents.
## Technical Stack
● Core Logic: Python
● AI/ML: Scikit-learn, Pandas, Joblib
● Explainability (LLM): Hugging Face Transformers, PyTorch, GPT-2
● UI & Visualization: Streamlit
● Version Control: Git

## Project Architecture & File Structure
The project is built with a clear, modular structure for maintainability and scalability.
SMARTUPDATE/
├── logs/
│ └── decisions.csv # Log of all agent actions and system states
├── models/
│ ├── predictive_model.pkl # Trained ML model for predictive analytics
│ ├── le_network.pkl # Encoder for network status
│ └── le_decision.pkl # Encoder for decision labels
│ └── user_idle_patterns.pkl # Learned user behavior patterns
├── pages/
│ ├── dashboard.py # Real-time multi-device monitoring dashboard
│ └── simulate_agent.py # Interactive simulation UI with sliders
├── config.py # Configuration constants (e.g., thresholds)
├── decision_engine.py # Rule-based decision logic
├── explain_ai.py # LLM-based explanation and resolution steps generator
├── logger.py # Module for logging all decisions to CSV
├── main.py # The central agent orchestrator and continuous simulation
loop
├── monitor.py # Generates realistic, time-based system status
├── patch_verifier.py # Simulates a dynamic patch stream and compatibility
checks
├── updater.py # Executes update actions, including failures and rollbacks
└── user_behavior_learner.py # Analyzes logs to identify user idle patterns

## Future Enhancements
● Real-world Integration: Connecting to actual system telemetry APIs and patch
management systems.
● Advanced LLM: Integrating a larger LLM (e.g., GPT-3.5/GPT-4) with a
Retrieval-Augmented Generation (RAG) system for fact-based resolution steps.
● Adaptive Scheduling: Developing a scheduler that predicts the next optimal
update time and proactively schedules deferred patches.
● Multi-Device Orchestration: Implementing a more robust architecture for
managing a large fleet of devices with a central database.
Contact

## LIVE DEMO 


## Project Lead: Vino ,Ganesh Kumar T
