from typing import List


# -------------------------------
# TASK-SPECIFIC GRADERS
# -------------------------------

def grade_easy(final_state: dict, history: List[str]) -> float:
    # Focus: emotion handling
    if "apologize" in history:
        return 1.0
    return 0.2


def grade_medium(final_state: dict, history: List[str]) -> float:
    # Focus: information gathering
    if "gather_info" in history and "act_now" in history:
        return 1.0
    elif "gather_info" in history:
        return 0.6
    return 0.3


def grade_hard(final_state: dict, history: List[str]) -> float:
    # Full decision quality
    ideal = ["apologize", "gather_info", "act_now"]

    if history[:3] == ideal:
        return 1.0

    score = 0.0

    # emotion handled
    if "apologize" in history:
        score += 0.3

    # uncertainty reduced
    if len(final_state["unknowns"]) == 0:
        score += 0.4

    # acted
    if "act_now" in history:
        score += 0.3

    return min(score, 1.0)


# -------------------------------
# MAIN DISPATCHER (CRITICAL)
# -------------------------------

def grade_task(task_id: str, final_state: dict, history: List[str]) -> float:

    if task_id == "task_easy":
        return grade_easy(final_state, history)

    elif task_id == "task_medium":
        return grade_medium(final_state, history)

    elif task_id == "task_hard":
        return grade_hard(final_state, history)

    return 0.0