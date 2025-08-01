# updater.py (Enhanced for Failure Simulation & Rollback)

import time
import random

def apply_update(patch_details=None, system_status=None):
    """
    Simulates applying an update. Now has a chance to randomly fail.
    Returns: True if successful, False if failed.
    """
    patch_id = patch_details.get('id', 'N/A') if patch_details else 'N/A'
    patch_size = patch_details.get('size_mb', 'N/A') if patch_details else 'N/A'
    requires_reboot = patch_details.get('requires_reboot', False) if patch_details else False
    
    # Simulate a 10% chance of failure (can be adjusted)
    is_successful = random.random() > 0.1

    if is_successful:
        msg = f"✅ Update for Patch {patch_id} applied successfully."
        msg += f" (Size: {patch_size}MB)."
        
        if requires_reboot:
            msg += " A system reboot is required for this update to take full effect."
            if system_status and system_status.get('user_active', False) == True:
                msg += " (Reboot will be scheduled for an idle period to avoid disruption)."
            else:
                msg += " (System will reboot shortly)."
        
        print(msg)
        time.sleep(2)
        return True
    else:
        # Failure scenario
        msg = f"❌ Error: Update for Patch {patch_id} failed during application."
        print(msg)
        time.sleep(2)
        return False

def postpone_update(reason_detail="Will retry later."):
    """
    Simulates postponing an update, with a more specific reason.
    """
    print(f"⏳ Update postponed. {reason_detail}")
    time.sleep(1)

def apply_mini_patch(patch_details=None, system_status=None):
    """
    Simulates applying a small, urgent "mini-patch" which might be faster or less disruptive.
    Returns: True if successful, False if failed. (simulating same failure rate as above)
    """
    patch_id = patch_details.get('id', 'N/A') if patch_details else 'N/A'

    is_successful = random.random() > 0.1 # Same failure chance
    
    if is_successful:
        print(f"⚡ Mini-patch {patch_id} applied quickly. (Less disruptive update).")
        time.sleep(1)
        return True
    else:
        print(f"❌ Error: Mini-patch {patch_id} failed during application.")
        time.sleep(1)
        return False


def defer_large_patch_and_schedule(patch_details=None, system_status=None):
    """
    Simulates deferring a large patch to a better time, explicitly.
    This action never "fails" as it's just a scheduling decision.
    """
    patch_id = patch_details.get('id', 'N/A') if patch_details else 'N/A'
    patch_size = patch_details.get('size_mb', 'N/A') if patch_details else 'N/A'
    print(f"➡️ Large patch {patch_id} ({patch_size}MB) deferred. Will schedule for an optimal time later.")
    time.sleep(1)

def rollback_update(patch_details=None):
    """
    Simulates the rollback process after a failed update.
    """
    patch_id = patch_details.get('id', 'N/A') if patch_details else 'N/A'
    print(f"⏪ Update for Patch {patch_id} failed. Initiating rollback to previous state.")
    time.sleep(3) # Rollback takes longer
    print(f"✅ Rollback of Patch {patch_id} complete. System is stable.")