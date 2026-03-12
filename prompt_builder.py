import json

def build_emotion_prompt(payload: dict):
    raw = payload.get("raw_signals", {}) or {}

    move_count = int(raw.get("move_count", 0))
    wrong_direction_count = int(raw.get("wrong_direction_count", 0))
    repeated_move_count = int(raw.get("repeated_move_count", 0))
    boxes_stuck_in_window = int(raw.get("boxes_stuck_in_window", 0))
    undos_in_window = int(raw.get("undos_in_window", 0))
    idle_time_ms = int(raw.get("idle_time_ms", 0))
    avg_time_between_moves_ms = int(raw.get("avg_time_between_moves_ms", 0))
    timing_std_ms = int(raw.get("timing_std_ms", 0))
    boxes_on_target_delta = int(raw.get("boxes_on_target_delta", 0))
    window_ms = int(raw.get("window_ms", 5000) or 5000)

    move_count = max(move_count, 1)

    major_errors = undos_in_window + boxes_stuck_in_window
    minor_errors = wrong_direction_count + repeated_move_count

    interaction_intensity = min(move_count / 30.0, 1.0)
    error_rate = min((major_errors * 1.0 + minor_errors * 0.5) / move_count, 1.0)
    pause_frequency = min(idle_time_ms / max(window_ms, 1), 1.0)
    interaction_instability = min(timing_std_ms / 500.0, 1.0)
    performance_quality = max(0.0, min(1.0, 1.0 - error_rate + (boxes_on_target_delta * 0.1)))

    metrics = {
        "performance_delta": round(boxes_on_target_delta / max(move_count, 1), 3),
        "error_rate": round(error_rate, 3),
        "recovery_speed": round(max(0.0, 1.0 - pause_frequency), 3),
        "action_frequency": round(interaction_intensity, 3),
        "input_variability": round(interaction_instability, 3),
        "risk_index": round(min((major_errors + minor_errors) / max(move_count, 1), 1.0), 3),
        "session_persistence": round(min(move_count / 50.0, 1.0), 3),
        "interaction_density": round(interaction_intensity, 3),
    }

    prompt = f"""
You are an expert psychologist.
Your task is to classify the user's emotion.
Do not only focus on one single feature, but analyze the whole context and patterns in the data.
Return ONLY a JSON object, don't include any other text or explanation, with the following fields:
- Emotion (one of the list below)
- Intensity (categories: Low, Medium, High)

Only when you are in doubt, return the two most likely emotions with their respective intensity and confidence.
In general return only one emotion, but if the data is ambiguous, return two. If you are not confident about any emotion, return 'No emotion'.

List of emotions:
- Stress
- Frustration
- Engagement
- Boredom
- Calm
- Cognitive_load

First of all, you will be receiving game telemetric data. Game metrics:
{json.dumps(metrics)}

Explanations for each of the metric features are as follows:
- Performance Delta: Change in performance relative to baseline (positive = better performance)
- Error Rate: Proportion of errors in the game session (0.0 = no errors, 1.0 = all actions are errors)
- Recovery Speed: Speed at which the player recovers from errors (higher = faster recovery)
- Action Frequency: How often the player performs actions (higher = more frequent actions)
- Input Variability: How varied the inputs are (higher = more varied inputs)
- Risk Index: How risky the player's decisions are (higher = more risky decisions)
- Session Persistence: How long the player continues playing (higher = longer sessions)
- Interaction Density: How many interactions occur per unit time (higher = more interactions)
""".strip()

    return prompt, metrics