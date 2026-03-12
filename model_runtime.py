import json
import re
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"

def get_device():
    if torch.backends.mps.is_available():
        return "mps"
    elif torch.cuda.is_available():
        return "cuda"
    return "cpu"

DEVICE = get_device()

if DEVICE in ["cuda", "mps"]:
    TORCH_DTYPE = torch.float16
else:
    TORCH_DTYPE = torch.float32

print(f"[model_runtime] Using device: {DEVICE}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

if DEVICE == "mps":
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=TORCH_DTYPE
    ).to(DEVICE)
elif DEVICE == "cuda":
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=TORCH_DTYPE,
        device_map="auto"
    )
else:
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        torch_dtype=TORCH_DTYPE
    ).to(DEVICE)

model.eval()

def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return None

def run_model(prompt: str) -> dict:
    inputs = tokenizer(prompt, return_tensors="pt")

    inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_new_tokens=120,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    generated_tokens = out[0][inputs["input_ids"].shape[1]:]
    text = tokenizer.decode(generated_tokens, skip_special_tokens=True)

    json_str = extract_json(text)
    if not json_str:
        return {
            "Emotion": "No emotion",
            "Intensity": "Low"
        }

    try:
        return json.loads(json_str)
    except Exception:
        return {
            "Emotion": "No emotion",
            "Intensity": "Low"
        }