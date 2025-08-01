# user_behavior_learner.py

import pandas as pd
import joblib
import os
from datetime import datetime

LOG_FILE = 'logs/decisions.csv'
LEARNED_PATTERNS_PATH = 'models/user_idle_patterns.pkl'

def learn_idle_patterns():
    """
    Analyzes decisions.csv to identify hours of the day when the user is typically idle.
    Saves a list of these 'idle hours'.
    """
    print("Learning user idle patterns from logs...")
    if not os.path.exists(LOG_FILE):
        print(f"Error: {LOG_FILE} not found. Cannot learn idle patterns.")
        return None

    try:
        df = pd.read_csv(LOG_FILE)
        # Ensure 'timestamp' is datetime and 'user_active' is boolean
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        # Rename 'user_active' to 'user_activity' if needed based on the actual CSV column name AFTER remapping logic
        # For simplicity here, assuming the CSV column that represents user activity is 'user_active' as per monitor.py and your CSV sample
        # If your CSV uses 'user_active', this is fine. If it logs 'user_activity' directly, adjust.
        # Based on your CSV sample: 'user_active' is the column name. So it's correct.

        # Extract hour of the day
        df['hour'] = df['timestamp'].dt.hour

        # Filter for instances where the user was NOT active (idle)
        idle_data = df[df['user_active'] == False]

        if idle_data.empty:
            print("No idle periods found in logs. Cannot learn patterns.")
            return None

        # Count occurrences of idle per hour
        idle_hour_counts = idle_data['hour'].value_counts().sort_index()

        # Determine "idle hours": for a prototype, let's pick hours that are frequently idle.
        # For simplicity, we can pick hours where idle count is above average, or a certain threshold.
        # Let's say we pick hours that occur in the top X% of idle times.
        # Or, just identify all hours where idle was recorded.
        
        # A simple approach for prototype: Identify hours that are idle at least once.
        # More sophisticated: identify hours where > 50% of recordings were idle.
        
        # Let's go with a simple threshold based on the number of idle recordings in that hour
        # For prototype, we'll consider hours with more than 1 occurrence of idle as potential idle hours
        
        # Calculate the average frequency of idle status across all hours present
        # Or, define a fixed threshold. Given limited data, a simpler approach is best.
        
        # Let's find hours where user_active is consistently false, or frequently false.
        # Group by hour and calculate the percentage of idle periods
        hourly_activity = df.groupby('hour')['user_active'].value_counts(normalize=True).unstack(fill_value=0)
        
        idle_hours_candidates = []
        if False in hourly_activity.columns: # Check if 'False' (idle) column exists
            # Identify hours where 'user_active' is False for more than a certain percentage of observations
            # For a small dataset, let's just consider hours where 'False' is the majority or close to it.
            # E.g., if more than 50% of the time in that hour, the user was idle.
            for hour, row in hourly_activity.iterrows():
                if False in row and row[False] > 0.5: # User was idle more than 50% of the time in this hour
                    idle_hours_candidates.append(hour)
        
        # If no hours meet the 50% criteria (common with random data), fallback to all hours with any idle.
        if not idle_hours_candidates and not idle_data.empty:
            idle_hours_candidates = sorted(idle_data['hour'].unique().tolist())
            print(f"Fallback: Identified all hours with any idle activity: {idle_hours_candidates}")
        elif idle_hours_candidates:
            print(f"Identified potential idle hours (over 50% idle): {sorted(idle_hours_candidates)}")
        
        learned_idle_patterns = {
            "idle_hours": sorted(idle_hours_candidates),
            "last_learned": datetime.now()
        }

        os.makedirs(os.path.dirname(LEARNED_PATTERNS_PATH), exist_ok=True)
        joblib.dump(learned_idle_patterns, LEARNED_PATTERNS_PATH)
        print(f"Learned idle patterns saved to {LEARNED_PATTERNS_PATH}")
        return learned_idle_patterns

    except Exception as e:
        print(f"Error learning idle patterns: {e}")
        return None

def get_idle_window_status(current_hour, learned_patterns):
    """
    Checks if the current_hour falls within a learned idle window.
    Returns True if idle, False otherwise.
    """
    if learned_patterns and learned_patterns.get("idle_hours"):
        return current_hour in learned_patterns["idle_hours"]
    return False

if __name__ == "__main__":
    # Example usage:
    # First, run your main.py a few times to generate some decisions.csv data
    # Then run this script to learn patterns.
    patterns = learn_idle_patterns()
    if patterns:
        print(f"\nLearned idle hours: {patterns['idle_hours']}")
        current_time = datetime.now()
        is_idle_window = get_idle_window_status(current_time.hour, patterns)
        print(f"Current hour ({current_time.hour}) is in idle window: {is_idle_window}")
    else:
        print("Could not load or learn idle patterns.")