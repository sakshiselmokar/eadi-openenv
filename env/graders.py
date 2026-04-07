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


def grade_task(task_id: str, history: List[str]) -> float:

    if task_id == "task_easy":
        return evaluate_emotion(history)

    elif task_id == "task_medium":
        return evaluate_sequence(history)

    elif task_id == "task_hard":
        return max(0.0, min(1.0, (
            0.4 * evaluate_sequence(history) +
            0.3 * evaluate_emotion(history) +
            0.3 * evaluate_efficiency(history, 4)
        )))

    return 0.0