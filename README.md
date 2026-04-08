---
title: EADI OpenEnv
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
sdk_version: "1.0"
app_port: 7860
app_file: app/main.py
pinned: false
---
# 🧠 EADI-OpenEnv

### Emotion-Aware Decision Intelligence Environment

---

## 🚀 Overview

EADI (Emotion-Aware Decision Intelligence) is a real-world OpenEnv environment designed to evaluate how AI agents make decisions under **emotional pressure, uncertainty, and time constraints**.

Unlike traditional environments that focus only on logic or accuracy, EADI introduces **human-centric decision dynamics**, where agents must:

* Understand emotional context
* Reduce uncertainty through information gathering
* Take timely and effective actions

---

## 🌍 Why This Matters

Real-world decision-making is rarely perfect or fully informed.

AI systems today are increasingly deployed in domains such as:

* Customer support systems
* Startup and business decision-making
* Healthcare response scenarios
* Crisis management tools

In these situations, **handling emotions + incomplete information + time pressure** is critical.

EADI provides a structured benchmark to evaluate such capabilities.

---

## 🧩 Environment Design

Each episode simulates a real-world scenario with:

* A user message
* Emotional state (angry, confused, anxious)
* Known facts vs unknown variables
* Limited time steps

The agent must navigate this environment by choosing appropriate actions.

---

## 🎮 Action Space

Agents can choose from:

* `apologize` → address emotional state
* `clarify` → partially stabilize situation
* `gather_info` → reduce uncertainty
* `act_now` → take final decision
* `delay` → postpone action (penalty)
* `ignore` → harmful action (penalty)

---

## 👁 Observation Space

Each step provides:

* User message
* Current emotion
* Context (startup, healthcare, tech, etc.)
* Known facts
* Unknown factors
* Remaining time
* Action history

---

## 🎯 Tasks

### 🟢 Task Easy — Emotion Stabilization

Goal: Reduce emotional distress
Focus: Correct emotional response

---

### 🟡 Task Medium — Information-Guided Decision

Goal: Gather necessary information before acting
Focus: Logical sequencing

---

### 🔴 Task Hard — Strategic Multi-Step Decision

Goal:

* Stabilize emotion
* Reduce uncertainty
* Take correct action

Focus: **multi-step reasoning under constraints**

---

## 🏆 Reward Design

The reward function provides **dense feedback**:

### Components:

* Emotion Score → handling user emotion
* Decision Score → correctness of actions
* Efficiency Score → optimal step usage

### Key Features:

* Partial rewards for progress
* Penalties for premature decisions
* Bonus for optimal action sequence

Example ideal sequence:

```text
apologize → gather_info → act_now
```

---

## 🤖 Baseline Agent

We provide a deterministic baseline agent that:

* Handles emotion first
* Gathers missing information
* Acts only when confident

This ensures:

* Reproducibility
* Stable evaluation
* No external dependency

---

## 🧪 Running the Environment

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run API server

```bash
python -m uvicorn app.main:app --reload
```

### 3. Test endpoints

* POST `/reset`
* POST `/step`
* GET `/state`

---

## 🐳 Docker

```bash
docker build -t eadi-openenv .
docker run -p 7860:7860 eadi-openenv
```

---

## 📊 Inference

```bash
python inference.py
```

Produces structured logs:

```
[START] ...
[STEP] ...
[END] ...
```

---

## 🧠 Key Contributions

* Emotion-aware RL environment
* Multi-step decision modeling
* Uncertainty-driven reasoning
* Sequence-sensitive reward system
* Fully OpenEnv compliant

---

## 🔮 Future Extensions

* Dynamic emotion transitions
* Multi-agent interaction
* Real-time streaming inputs
* Integration with LLM-based policies (e.g., Gemma family models)

---

## 🏁 Conclusion

EADI moves beyond traditional benchmarks by evaluating **how agents behave in human-like decision environments**, not just what answers they produce.

It serves as a step toward **more reliable, context-aware, and human-aligned AI systems**.
