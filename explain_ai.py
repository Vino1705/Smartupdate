# explain_ai.py (Upgraded for Improved LLM Quality)

from transformers import pipeline, set_seed

# Initialize the text generation pipeline with a slightly larger, more capable model
# 'gpt2' is a good step up from 'distilgpt2' for better quality output.
try:
    generator = pipeline("text-generation", model="gpt2")
    set_seed(42) # For reproducibility of generated text
    LLM_READY = True
    print("LLM (gpt2) for explanations loaded successfully.")
except Exception as e:
    print(f"Warning: Could not load gpt2 for explanations: {e}. LLM explanations will be disabled.")
    LLM_READY = False
    # Define a dummy generator if LLM fails to load
    class DummyGenerator:
        def __call__(self, prompt, **kwargs):
            return [{"generated_text": prompt + "\nExplanation: LLM failed to load. No explanation available."}]
    generator = DummyGenerator()


def generate_explanation(system_status, action, reason):
    """
    Generates a human-readable explanation for the update decision.
    """
    if not LLM_READY:
        return f"⚠️ LLM explanation failed: LLM not loaded. (Action: {action}, Reason: {reason})"

    # Refined prompt for better explanation quality
    prompt = (
        f"Give a short, polite explanation (with emojis) for why the system decided to {action.lower()} the update. "
        f"The reason is: {reason}.\nExplanation:"
    )

    try:
        output = generator(
            prompt,
            max_new_tokens=70, # Increased for more comprehensive explanation
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            pad_token_id=generator.tokenizer.eos_token_id,
            truncation=True
        )
        generated = output[0]["generated_text"]
        explanation = generated.split("Explanation:")[-1].strip()
        # Clean up potential repetitive output from gpt2
        return explanation.split("\n\n")[0].strip()
    except Exception as e:
        return f"⚠️ LLM explanation failed: {e}"


def generate_resolution_steps(reason, system_status):
    """
    Generates actionable steps to resolve the issue for a postponed update.
    """
    if not LLM_READY:
        return "LLM not loaded. No specific resolution steps available."

    # More detailed prompt with request for a numbered list
    system_status_str = ", ".join([f"{k}: {v}" for k, v in system_status.items()])

    # Adjust prompt for specific common reasons for better quality output
    if "No internet connection" in reason:
        specific_prompt = f"The update was postponed because there is no internet connection. To resolve this, provide a numbered list of clear steps. Resolution steps:"
    elif "Battery too low" in reason:
        specific_prompt = f"The update was postponed because the battery level is {system_status.get('battery_level', 'unknown')}%. To resolve this, provide a numbered list of clear steps. Resolution steps:"
    elif "System busy or user active" in reason:
        specific_prompt = f"The update was postponed because the system is busy or the user is active (CPU: {system_status.get('cpu_usage', 'unknown')}%, User Active: {system_status.get('user_active', 'unknown')}). To resolve this, provide a numbered list of clear steps. Resolution steps:"
    elif "Patch incompatible" in reason:
        specific_prompt = f"The update was postponed because the patch is incompatible ({system_status.get('compatibility_reason', 'no specific reason')}). To resolve this, provide a numbered list of clear steps. Resolution steps:"
    else:
        specific_prompt = f"The update was postponed because: {reason}. Provide a numbered list of concise, actionable steps based on system status: {system_status_str}. Resolution steps:"

    try:
        output = generator(
            specific_prompt,
            max_new_tokens=120, # More tokens for resolution steps
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            pad_token_id=generator.tokenizer.eos_token_id,
            truncation=True
        )
        generated = output[0]["generated_text"]
        resolution_steps = generated.split("Resolution steps:")[-1].strip()
        # Basic cleanup
        resolution_steps = resolution_steps.split("The update was postponed because")[0].strip()
        return resolution_steps
    except Exception as e:
        return f"⚠️ LLM failed to generate resolution steps: {e}"