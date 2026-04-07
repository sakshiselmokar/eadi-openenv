import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from env.models import Observation
from env.environment import EADIEnvironment
from env.models import Action
from env.graders import grade_task

# history = ["apologize", "gather_info", "act_now"]
history = ["ignore", "delay"]
print("Easy:", grade_task("task_easy", history))
print("Medium:", grade_task("task_medium", history))
print("Hard:", grade_task("task_hard", history))