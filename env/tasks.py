from typing import Dict


# -------------------------------
# TASK DEFINITIONS
# -------------------------------
TASKS = {
    "task_easy": {
        "description": "Emotion Stabilization Task",
        "goal": "Reduce user emotional distress",
        "max_steps": 2
    },
    "task_medium": {
        "description": "Information-Guided Decision Task",
        "goal": "Gather relevant information before taking action",
        "max_steps": 3
    },
    "task_hard": {
        "description": "Multi-step Strategic Decision Task",
        "goal": "Balance emotional handling, uncertainty reduction, and correct final decision",
        "max_steps": 4
    }
}