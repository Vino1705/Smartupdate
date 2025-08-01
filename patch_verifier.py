# patch_verifier.py (Enhanced for Dynamic Patch Stream Simulation)

import random

# Mock database of "patches" is now a list of pre-defined patch dictionaries
MOCK_PATCH_STREAM = [
    {"id": "patch_A_v1.2", "criticality_score": 10, "vulnerability_details": "CVE-2024-001: Critical remote code execution vulnerability.", "type": "security", "requires_reboot": True, "min_cpu": 20, "min_battery": 30, "size_mb": 150},
    {"id": "patch_B_v2.0", "criticality_score": 7, "vulnerability_details": "CVE-2024-002: High-severity bug allowing privilege escalation.", "type": "feature", "requires_reboot": False, "min_cpu": 10, "min_battery": 20, "size_mb": 50},
    {"id": "patch_C_v1.1", "criticality_score": 4, "vulnerability_details": "Minor bug fix for UI rendering.", "type": "bugfix", "requires_reboot": False, "min_cpu": 5, "min_battery": 15, "size_mb": 20},
    {"id": "patch_D_v3.0", "criticality_score": 1, "vulnerability_details": "Performance update and new emoji pack.", "type": "bugfix", "requires_reboot": False, "min_cpu": 5, "min_battery": 10, "size_mb": 10},
    {"id": "patch_E_v4.5", "criticality_score": 10, "vulnerability_details": "CVE-2024-003: Critical data exfiltration vulnerability.", "type": "security", "requires_reboot": True, "min_cpu": 50, "min_battery": 50, "size_mb": 300},
    {"id": "patch_F_v1.0", "criticality_score": 7, "vulnerability_details": "Hotfix for a denial-of-service vulnerability.", "type": "security", "requires_reboot": False, "min_cpu": 5, "min_battery": 15, "size_mb": 5},
]

# We will "fetch" patches from this list in order, cycling through it
patch_stream_index = 0

def get_latest_patch():
    """
    Simulates fetching the next patch from a central patch management system.
    Cycles through a predefined list of mock patches.
    """
    global patch_stream_index
    patch_details = MOCK_PATCH_STREAM[patch_stream_index]
    patch_stream_index = (patch_stream_index + 1) % len(MOCK_PATCH_STREAM)
    return patch_details

def check_patch_compatibility(patch_details, system_status):
    """
    Checks if a given patch is compatible with the current system status.
    Returns (is_compatible: bool, compatibility_reason: str).
    """
    reasons = []
    compatible = True

    if system_status["cpu_usage"] < patch_details["min_cpu"]:
        compatible = False
        reasons.append(f"CPU usage ({system_status['cpu_usage']}%) is below required minimum ({patch_details['min_cpu']}%).")

    if system_status["battery_level"] < patch_details["min_battery"]:
        compatible = False
        reasons.append(f"Battery level ({system_status['battery_level']}%) is below required minimum ({patch_details['min_battery']}%).")

    if system_status["network"] == "offline" and patch_details["size_mb"] > 0:
         compatible = False
         reasons.append(f"Network is offline, cannot download patch.")

    if compatible:
        return True, "All compatibility checks passed."
    else:
        return False, "; ".join(reasons)

def get_patch_risk_and_compatibility(system_status):
    """
    Generates a patch from the dynamic stream and assesses its risk and compatibility.
    """
    patch_details = get_latest_patch()
    
    security_risk_score = patch_details["criticality_score"]

    is_compatible, compatibility_reason = check_patch_compatibility(patch_details, system_status)

    return patch_details["id"], patch_details, security_risk_score, is_compatible, compatibility_reason

if __name__ == "__main__":
    # Example usage:
    from monitor import get_system_status
    print("--- Dynamic Patch Stream Test ---")
    for _ in range(8): # Test for 8 cycles
        current_status = get_system_status()
        patch_id, patch_details, security_risk, is_compatible, compat_reason = \
            get_patch_risk_and_compatibility(current_status)
        
        print(f"\nPatch: {patch_id}")
        print(f"  Vulnerability: {patch_details['vulnerability_details']}")
        print(f"  Security Score: {security_risk}")
        print(f"  Compatibility: {is_compatible} | Reason: {compat_reason}")