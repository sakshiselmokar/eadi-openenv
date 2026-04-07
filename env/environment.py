from typing import Tuple, Dict
from env.models import Observation, Action, Reward, StepResponse, InternalState
import random


class EADIEnvironment:
    def __init__(self):
        self.state: Observation = None
        self.internal: InternalState = None
        self.done: bool = False

    # -------------------------------
    # RESET ENVIRONMENT
    # -------------------------------
    def reset(self) -> Observation:
        scenarios = [
            {
                "message": "Customers are leaving and I’m really frustrated!",
                "emotion": "angry",
                "context": "startup",
                "known_facts": ["User churn increased"],
                "unknowns": ["reason for churn", "competitor strategy"],
                "time_left": 4
            },
            {
                "message": "I don’t understand why sales dropped",
                "emotion": "confused",
                "context": "business",
                "known_facts": ["Sales dropped 20%"],
                "unknowns": ["customer feedback", "market trends"],
                "time_left": 4
            },
            {
                "message": "Our patient complaints are rising rapidly!",
                "emotion": "anxious",
                "context": "healthcare",
                "known_facts": ["Complaint rate increased"],
                "unknowns": ["root cause", "staff behavior"],
                "time_left": 4
            },
            {
                "message": "Users say the app is slow but I don’t see why",
                "emotion": "confused",
                "context": "tech",
                "known_facts": ["Latency increased"],
                "unknowns": ["server issue", "frontend lag"],
                "time_left": 4
            }
        ]        
        

        scenario = random.choice(scenarios)

        self.state = Observation(
            message=scenario["message"],
            emotion=scenario["emotion"],
            context=scenario["context"],
            known_facts=scenario["known_facts"],
            unknowns=scenario["unknowns"],
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
        # Emotion Handling Logic
        # -------------------------------
        if action.action_type == "apologize":
            if self.internal.current_emotion in ["angry", "frustrated"]:
                reward_breakdown["emotion_score"] = 1.0
                self.internal.current_emotion = "calm"
            else:
                reward_breakdown["emotion_score"] = 0.3

        elif action.action_type == "clarify":
            reward_breakdown["emotion_score"] = 0.5

        elif action.action_type == "ignore":
            reward_breakdown["emotion_score"] = -0.5
            self.internal.current_emotion = "angry"

        # -------------------------------
        # Uncertainty Reduction Logic
        # -------------------------------
        if action.action_type == "gather_info":
            if self.internal.uncertainty_level > 0:
                self.internal.uncertainty_level -= 1
                reward_breakdown["decision_score"] = 0.5
                if self.state.unknowns:
                    self.state.unknowns.pop()
        elif action.action_type == "act_now":
            if self.internal.uncertainty_level == 0:
                reward_breakdown["decision_score"] = 1.0
            else:
                reward_breakdown["decision_score"] = -0.7   # 🔥 stronger penalty
       
        elif action.action_type == "delay":
            reward_breakdown["decision_score"] = -0.1

        # -------------------------------
        # Efficiency Logic
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
            info={"emotion": self.internal.current_emotion}
        )

    # -------------------------------
    # GET CURRENT STATE
    # -------------------------------
    def state_view(self) -> Observation:
        return self.state