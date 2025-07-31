# explain_ai.py
from transformers import pipeline, set_seed

generator = pipeline("text-generation", model="distilgpt2")
set_seed(42)

def generate_explanation(system_status, action, reason):
    prompt = (
        f"Give a short, polite explanation (with emojis) for why the system decided to {action.lower()} the update. "
        f"The reason is: {reason}.\nExplanation:"
    )

    try:
        output = generator(
            prompt,
            max_new_tokens=50,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            pad_token_id=50256,
            truncation=True
        )
        generated = output[0]["generated_text"]
        explanation = generated.split("Explanation:")[-1].strip()
        return explanation
    except Exception as e:
        return f"⚠️ Hugging Face explanation failed: {e}"
