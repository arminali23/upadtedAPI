from datetime import datetime, timezone
from prompt_builder import build_emotion_prompt
from model_runtime import run_model

def predict(payload: dict) -> dict:
    prompt, metrics = build_emotion_prompt(payload)
    model_output = run_model(prompt)

    session_id = payload.get("session_id") or payload.get("scenario_id") or "UNKNOWN"
    timestamp = datetime.now(timezone.utc).isoformat()

    return {
        "session_id": session_id,
        "timestamp": timestamp,
        "input_metrics": metrics,
        "prediction": model_output,
        "echo": payload
    }