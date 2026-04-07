from fastapi import FastAPI
from env.environment import EADIEnvironment
from env.models import Action

app = FastAPI()

env = EADIEnvironment()


# Allow both GET and POST for /reset
@app.api_route("/reset", methods=["GET", "POST"])
def reset():
    obs = env.reset()
    return {
        "observation": obs.dict(),
        "done": False
    }


# Allow both GET and POST for /step
@app.api_route("/step", methods=["GET", "POST"])
def step(action: dict = None):
    if action is None:
        # Default action if GET request (optional: return error instead)
        return {"error": "Action data required for step endpoint."}

    act = Action(**action)
    result = env.step(act)

    return {
        "observation": result.observation.dict(),
        "reward": result.reward.score,
        "done": result.done,
        "info": result.info
    }


# Allow both GET and POST for /state
@app.api_route("/state", methods=["GET", "POST"])
def state():
    obs = env.state_view()
    return obs.dict()