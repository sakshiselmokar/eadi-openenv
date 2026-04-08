from typing import List


def evaluate_sequence(history: List[str]) -> float:
    ideal = ["apologize", "gather_info", "act_now"]

    if history[:3] == ideal:
        return 1.0
    elif "act_now" in history and "gather_info" not in history:
        return 0.2
    elif "gather_info" in history:
        return 0.6
    return 0.0


def evaluate_emotion(history: List[str]) -> float:
    if "apologize" in history:
        return 1.0
    return 0.0


def evaluate_efficiency(history: List[str], max_steps: int) -> float:
    return 1.0 if len(history) <= max_steps else 0.5

def grade_task(task_id: str, final_state: dict, history: list) -> float:
    score = 0.0

    # Emotion stability
    if final_state["emotion"] in ["calm", "neutral"]:
        score += 0.4

    # Uncertainty resolution
    if len(final_state["unknowns"]) == 0:
        score += 0.4

    # Efficiency
    if len(history) <= 3:
        score += 0.2

    return max(0.0, min(1.0, score))

