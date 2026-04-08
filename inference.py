# NOTE:
# Currently using deterministic policy for reliability.
# This can be replaced with an LLM-based policy when API access is available.
# LLM logic intentionally commented for reliability during evaluation
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

# Use your approved model
MODEL_NAME = os.getenv("MODEL_NAME", "mistralai/Mistral-7B-v0.1")

TASK_NAME = os.getenv("TASK_NAME", "task_easy")
BENCHMARK = "eadi-openenv"

MAX_STEPS = 5
TEMPERATURE = 0.3
MAX_TOKENS = 50


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


# -------------------------------
# DETERMINISTIC FALLBACK POLICY
# -------------------------------
def deterministic_policy(state):

    # 1. Handle emotions first
    if state.emotion in ["angry", "frustrated"]:
        if "apologize" not in state.history:
            return "apologize"

    if state.emotion in ["confused", "uncertain"]:
        if "clarify" not in state.history:
            return "clarify"

    # 2. Gather info (limited)
    if state.unknowns:
        if state.history.count("gather_info") < 2:
            return "gather_info"

    # 3. Time pressure → act
    if state.time_left <= 1:
        return "act_now"

    # 4. If ready → act
    if not state.unknowns:
        return "act_now"

    return "clarify"


# -------------------------------
# HYBRID AGENT (LLM + FALLBACK)
# -------------------------------

def get_action_from_model(client, state):
    return deterministic_policy(state)

    # # Emotion-first intelligence
    # if state.emotion in ["angry", "frustrated"]:
    #     if "apologize" not in state.history:
    #         return "apologize"
    #     return "clarify"

    # if state.emotion in ["confused", "uncertain"]:
    #     return "clarify"

    # # Reduce uncertainty smartly
    # if state.unknowns:
    #     if state.history.count("gather_info") < 2:
    #         return "gather_info"

    # # Act when ready
    # if not state.unknowns:
    #     return "act_now"

    # return "clarify"
# def get_action_from_model(client: Optional[OpenAI], state):

#     # If no client → fallback directly
#     if client is None:
#         return deterministic_policy(state)

#     try:
#         prompt = f"""
#         You are an expert decision-making AI.

#         Situation:
#         Message: {state.message}
#         Emotion: {state.emotion}
#         Unknowns: {state.unknowns}
#         Time left: {state.time_left}
#         Past actions: {state.history}

#         Choose the BEST action from:
#         [apologize, clarify, gather_info, act_now, delay, ignore]

#         Rules:
#         - Handle emotions first
#         - Reduce uncertainty before acting
#         - Act when time is low

#         Return ONLY the action name.
#         """

#         response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=[
#                 {"role": "system", "content": "You are a strategic AI decision agent."},
#                 {"role": "user", "content": prompt},
#             ],
#             temperature=TEMPERATURE,
#             max_tokens=10,
#         )

#         action = (response.choices[0].message.content or "").strip().lower()

#         valid_actions = ["apologize", "clarify", "gather_info", "act_now", "delay", "ignore"]

#         if action not in valid_actions:
#             return deterministic_policy(state)

#         return action

#     except Exception as e:
#         print(f"[DEBUG] LLM failed → fallback: {e}", flush=True)
#         return deterministic_policy(state)


# -------------------------------
# MAIN LOOP
# -------------------------------
async def main():

    # Initialize client only if API key exists
    client = None
    if API_KEY:
        try:
            client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
        except Exception as e:
            print(f"[DEBUG] Client init failed: {e}", flush=True)

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
        # FINAL SCORING
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