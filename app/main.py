from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from env.environment import EADIEnvironment
from env.models import Action
from env.graders import grade_task
print("🔥 APP STARTED SUCCESSFULLY")
import os
from typing import List

app = FastAPI()
print("✅ APP CREATED")
# ✅ IMPORTANT for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": "App is running!"}

env = EADIEnvironment()

# -------------------------------
# CONFIG
# -------------------------------
MAX_STEPS = 5
TASK_NAME = os.getenv("TASK_NAME", "task_easy")


# -------------------------------
# POLICY (YOUR AGENT)
# -------------------------------
def deterministic_policy(state):

    if state.emotion in ["angry", "frustrated"]:
        if "apologize" not in state.history:
            return "apologize"

    if state.emotion in ["confused", "uncertain"]:
        if "clarify" not in state.history:
            return "clarify"

    if state.unknowns:
        if state.history.count("gather_info") < 2:
            return "gather_info"

    if state.time_left <= 1:
        return "act_now"

    if not state.unknowns:
        return "act_now"

    return "clarify"


# -------------------------------
# BASIC ENDPOINTS
# -------------------------------

@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "observation": obs.dict(),
        "done": False
    }


@app.post("/step")
def step(action: dict):
    act = Action(**action)
    result = env.step(act)

    return {
        "observation": result.observation.dict(),
        "reward": result.reward.score,
        "done": result.done,
        "info": result.info
    }


@app.get("/state")
def state():
    obs = env.state_view()
    return obs.dict()


# -------------------------------
# 🚀 AUTONOMOUS AI ENDPOINT
# -------------------------------

@app.post("/run-agent")
def run_agent():

    state = env.reset()

    trajectory = []
    rewards: List[float] = []
    history: List[str] = []

    for step_num in range(1, MAX_STEPS + 1):

        action_str = deterministic_policy(state)
        action = Action(action_type=action_str)

        result = env.step(action)

        step_data = {
            "step": step_num,
            "action": action_str,
            "reward": result.reward.score,
            "observation": result.observation.dict(),
            "done": result.done
        }

        trajectory.append(step_data)
        rewards.append(result.reward.score)
        history.append(action_str)

        state = result.observation

        if result.done:
            break

    # final scoring
    final_state = {
        "emotion": state.emotion,
        "unknowns": state.unknowns
    }

    score = grade_task(TASK_NAME, final_state, history)    
    success = score > 0.5

    return {
        "trajectory": trajectory,
        "final_score": score,
        "success": success,
        "steps_taken": len(trajectory),
        "total_reward": sum(rewards)
    }

print("🚀 REGISTERED ROUTES:")
for route in app.routes:
    print(route.path)