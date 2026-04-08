import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from env.models import Observation
from env.environment import EADIEnvironment
from env.models import Action
from env.graders import grade_task
env = EADIEnvironment()
state = env.reset(task="task_hard")

for _ in range(5):
    action = Action(action_type="ignore")  # bad action
    result = env.step(action)
    print(result)
    if result.done:
        break