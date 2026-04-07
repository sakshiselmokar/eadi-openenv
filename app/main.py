from fastapi import FastAPI
from env.environment import EADIEnvironment
from env.models import Action

app = FastAPI()

env = EADIEnvironment()


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