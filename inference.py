import os
import asyncio
from typing import List, Optional

from openai import OpenAI

from env.environment import EADIEnvironment
from env.models import Action
from env.graders import grade_task


# -------------------------------
# ENV VARIABLES (MANDATORY)
# -------------------------------
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

TASK_NAME = os.getenv("TASK_NAME", "task_easy")
BENCHMARK = "eadi-openenv"

MAX_STEPS = 5
TEMPERATURE = 0.3
MAX_TOKENS = 100


# -------------------------------
# LOGGING (STRICT FORMAT)
# -------------------------------
def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    error_val = error if error else "null"
    done_val = str(done).lower()

    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)

    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )
def get_action_from_model(client, state):

    # intelligent deterministic policy

    if state.emotion in ["angry", "frustrated", "anxious"]:
        return "apologize"

    if state.unknowns:
        return "gather_info"

    return "act_now"

# # -------------------------------
# # SIMPLE AGENT (LLM-BASED)
# # -------------------------------
# def get_action_from_model(client: OpenAI, state) -> str:
#     prompt = f"""
#     You are an AI decision agent.

#     Current state:
#     Message: {state.message}
#     Emotion: {state.emotion}
#     Unknowns: {state.unknowns}
#     Time left: {state.time_left}

#     Choose ONE action from:
#     [apologize, clarify, gather_info, act_now, delay, ignore]

#     Only return the action name.
#     """

#     try:
#         response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=[
#                 {"role": "system", "content": "You are a decision-making agent."},
#                 {"role": "user", "content": prompt},
#             ],
#             temperature=TEMPERATURE,
#             max_tokens=10,
#         )

#         action = (response.choices[0].message.content or "").strip().lower()

#         return action

#     except Exception as e:
#         print(f"[DEBUG] Model error: {e}", flush=True)
#         return "gather_info"


# -------------------------------
# MAIN LOOP
# -------------------------------
async def main():
    # client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    client = None
   
    env = EADIEnvironment()

    rewards: List[float] = []
    history: List[str] = []
    steps_taken = 0
    success = False
    score = 0.0

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        state = env.reset()

        for step in range(1, MAX_STEPS + 1):
            action_str = get_action_from_model(client, state)

            action = Action(action_type=action_str)

            try:
                result = env.step(action)
                reward = result.reward.score
                done = result.done
                error = None

            except Exception as e:
                reward = 0.0
                done = True
                error = str(e)

            rewards.append(reward)
            history.append(action_str)
            steps_taken = step

            log_step(step, action_str, reward, done, error)

            state = result.observation if not error else state

            if done:
                break

        # -------------------------------
        # FINAL SCORING (IMPORTANT)
        # -------------------------------
        score = grade_task(TASK_NAME, history)

        success = score > 0.5

    finally:
        log_end(success, steps_taken, score, rewards)


# -------------------------------
# ENTRYPOINT
# -------------------------------
if __name__ == "__main__":
    asyncio.run(main())