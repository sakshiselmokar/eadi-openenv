from pydantic import BaseModel, Field
from typing import List, Dict, Optional


# -------------------------------
# Observation Model (State)
# -------------------------------
class Observation(BaseModel):
    message: str
    emotion: str
    context: str
    known_facts: List[str]
    unknowns: List[str]
    time_left: int
    history: List[str] = Field(default_factory=list)


# -------------------------------
# Action Model
# -------------------------------
class Action(BaseModel):
    action_type: str  # e.g. apologize, clarify, gather_info, act_now


# -------------------------------
# Reward Model
# -------------------------------
class Reward(BaseModel):
    score: float  # 0.0 to 1.0
    breakdown: Dict[str, float]  # emotion_score, decision_score, efficiency_score


# -------------------------------
# Step Response Model
# -------------------------------
class StepResponse(BaseModel):
    observation: Observation
    reward: Reward
    done: bool
    info: Dict[str, Optional[str]] = Field(default_factory=dict)


# -------------------------------
# Internal State (Hidden Dynamics)
# -------------------------------
class InternalState(BaseModel):
    current_emotion: str
    uncertainty_level: int  # number of unknowns
    steps_taken: int