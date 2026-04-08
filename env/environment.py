from typing import Tuple, Dict
from env.models import Observation, Action, Reward, StepResponse, InternalState
import random


class EADIEnvironment:
    def __init__(self):
        self.state: Observation = None
        self.internal: InternalState = None
        self.done: bool = False
        self.task: str = "task_easy"
        self.scenario_meta: Dict = {}

    # -------------------------------
    # RESET ENVIRONMENT
    # -------------------------------
    def reset(self, task: str = "task_easy") -> Observation:
        self.task = task

        scenarios = [
            {
                "type": "startup_crisis",
                "risk": "high",
                "message": "Customers are leaving and I’m really frustrated!",
                "emotion": "angry",
                "context": "startup",
                "known_facts": ["User churn increased"],
                "unknowns": ["reason for churn", "competitor strategy"],
                "time_left": 3
            },
            {
                "type": "investor_call",
                "risk": "medium",
                "message": "Revenue is below expectations. Explain this.",
                "emotion": "neutral",
                "context": "business",
                "known_facts": ["Revenue dropped 20%"],
                "unknowns": ["investor expectations", "market trend"],
                "time_left": 3
            },
            {
                "type": "customer_complaint",
                "risk": "low",
                "message": "Your service is disappointing lately.",
                "emotion": "frustrated",
                "context": "support",
                "known_facts": ["Recent delays"],
                "unknowns": ["root cause"],
                "time_left": 3
            }
        ]

        scenario = random.choice(scenarios)
        self.scenario_meta = scenario

        # Task-specific difficulty
        if self.task == "task_hard":
            scenario["time_left"] = 2
            scenario["unknowns"].append("hidden risk factor")

        self.state = Observation(
            message=scenario["message"],
            emotion=scenario["emotion"],
            context=scenario["context"],
            known_facts=scenario["known_facts"],
            unknowns=list(scenario["unknowns"]),
            time_left=scenario["time_left"],
            history=[]
        )

        self.internal = InternalState(
            current_emotion=scenario["emotion"],
            uncertainty_level=len(scenario["unknowns"]),
            steps_taken=0
        )

        self.done = False
        return self.state

    # -------------------------------
    # STEP FUNCTION
    # -------------------------------
    def step(self, action: Action) -> StepResponse:
        if self.done:
            raise Exception("Episode is done. Call reset().")

        self.internal.steps_taken += 1
        self.state.time_left -= 1
        self.state.history.append(action.action_type)

        reward_breakdown = {
            "emotion_score": 0.0,
            "decision_score": 0.0,
            "efficiency_score": 0.0
        }

        # -------------------------------
        # ENVIRONMENT DRIFT (NEW 🔥)
        # -------------------------------
        if self.internal.current_emotion == "angry":
            if random.random() < 0.3:
                self.internal.uncertainty_level += 1
                self.state.unknowns.append("new issue surfaced")

        # -------------------------------
        # EMOTION LOGIC
        # -------------------------------
        if action.action_type == "apologize":
            if self.internal.current_emotion in ["angry", "frustrated"]:
                reward_breakdown["emotion_score"] = random.uniform(0.7, 1.0)
                self.internal.current_emotion = "calm"
            else:
                reward_breakdown["emotion_score"] = 0.3

        elif action.action_type == "clarify":
            reward_breakdown["emotion_score"] = 0.5

        elif action.action_type == "ignore":
            reward_breakdown["emotion_score"] = -0.6
            self.internal.current_emotion = "angry"
            self.internal.uncertainty_level += 2

        # -------------------------------
        # DECISION LOGIC
        # -------------------------------
        if action.action_type == "gather_info":
            if self.internal.uncertainty_level > 0:
                self.internal.uncertainty_level -= 1
                reward_breakdown["decision_score"] = 0.6
                if self.state.unknowns:
                    self.state.unknowns.pop()

        elif action.action_type == "act_now":
            if self.internal.uncertainty_level == 0:
                reward_breakdown["decision_score"] = 1.0
            else:
                reward_breakdown["decision_score"] = -0.4

        elif action.action_type == "delay":
            reward_breakdown["decision_score"] = -0.2

        # -------------------------------
        # FAILURE CONDITION (NEW 🔥)
        # -------------------------------
        if self.internal.current_emotion == "angry" and self.internal.uncertainty_level > 3:
            self.done = True

        # -------------------------------
        # EFFICIENCY
        # -------------------------------
        if self.state.time_left <= 0:
            self.done = True

        if self.internal.steps_taken <= 3:
            reward_breakdown["efficiency_score"] = 0.5
        else:
            reward_breakdown["efficiency_score"] = 0.2

        # -------------------------------
        # FINAL REWARD
        # -------------------------------
        final_score = (
            0.3 * reward_breakdown["emotion_score"] +
            0.4 * reward_breakdown["decision_score"] +
            0.3 * reward_breakdown["efficiency_score"]
        )

        final_score = max(0.0, min(1.0, final_score))

        reward = Reward(score=final_score, breakdown=reward_breakdown)
        return StepResponse(
            observation=self.state,
            reward=reward,
            done=self.done,
            info={
                "emotion": str(self.internal.current_emotion),
                "uncertainty": str(self.internal.uncertainty_level),
                "steps_taken": str(self.internal.steps_taken)
            }
        )
        

    def state_view(self) -> Observation:
        return self.state