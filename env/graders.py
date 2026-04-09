from typing import List


# helper to enforce strict (0,1)
def normalize(score: float) -> float:
    if score <= 0.0:
        return 0.01
    if score >= 1.0:
        return 0.99
    return score


# -------------------------------
# TASK-SPECIFIC GRADERS
# -------------------------------

def grade_easy(final_state: dict, history: List[str]) -> float:
    if "apologize" in history:
        return 0.95   # instead of 1.0
    return 0.2


def grade_medium(final_state: dict, history: List[str]) -> float:
    if "gather_info" in history and "act_now" in history:
        return 0.9    # instead of 1.0
    elif "gather_info" in history:
        return 0.6
    return 0.3


def grade_hard(final_state: dict, history: List[str]) -> float:
    ideal = ["apologize", "gather_info", "act_now"]

    if history[:3] == ideal:
        return 0.95   # instead of 1.0

    score = 0.0

    if "apologize" in history:
        score += 0.3

    if len(final_state["unknowns"]) == 0:
        score += 0.4

    if "act_now" in history:
        score += 0.3

    return normalize(score)


# -------------------------------
# MAIN DISPATCHER
# -------------------------------

def grade_task(task_id: str, final_state: dict, history: List[str]) -> float:

    if task_id == "task_easy":
        return normalize(grade_easy(final_state, history))

    elif task_id == "task_medium":
        return normalize(grade_medium(final_state, history))

    elif task_id == "task_hard":
        return normalize(grade_hard(final_state, history))

    return 0.01   # instead of 0.0