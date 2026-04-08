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

## 🚀 Live Demo

### 🌐 Interactive Frontend
👉 https://eadi-mindscape.vercel.app/

### ⚙️ API (Swagger UI)
👉 https://practiceof-eadi-openenv.hf.space/docs  

---

## 🎥 Demo Video

👉 https://youtu.be/2wkTwWpMnK0 
```



````

---

## 🌍 Overview

**EADI (Emotion-Aware Decision Intelligence)** is a next-generation AI evaluation environment designed to test how intelligent agents make decisions under:

- 😡 Emotional pressure  
- ❓ Uncertainty  
- ⏳ Time constraints  

Unlike traditional benchmarks, EADI simulates **human-like decision scenarios**, where correctness alone is not enough — **timing, empathy, and reasoning matter**.

---

## 💡 Why This Matters

Modern AI systems operate in real-world domains like:

- 🧑‍💼 Customer Support  
- 🏥 Healthcare Response  
- 🚨 Crisis Management  
- 📈 Business Decision-Making  

These environments involve:
- Incomplete information  
- Emotional users  
- Urgent decisions  

👉 EADI evaluates **how AI behaves**, not just what it predicts.

---

## 🧩 Environment Design

Each episode simulates a real-world interaction:

- User message  
- Emotional state *(angry, confused, anxious)*  
- Known facts vs unknowns  
- Limited decision steps  

Agents must balance:
> 🧠 Logic + ❤️ Empathy + ⚡ Timing

---

## 🎮 Action Space

| Action        | Purpose |
|--------------|--------|
| `apologize`  | Handle emotional distress |
| `clarify`    | Improve understanding |
| `gather_info`| Reduce uncertainty |
| `act_now`    | Make final decision |
| `delay`      | Postpone (penalty) |
| `ignore`     | Harmful (penalty) |

---

## 👁 Observation Space

At each step, agents receive:

- User message  
- Emotion  
- Context  
- Known facts  
- Unknowns  
- Time remaining  
- Action history  

---

## 🎯 Tasks

### 🟢 Easy — Emotion Stabilization  
Focus: Respond correctly to emotional signals  

### 🟡 Medium — Information-Guided Decision  
Focus: Gather missing info before acting  

### 🔴 Hard — Strategic Multi-Step Reasoning  
Focus:
- Emotional handling  
- Uncertainty reduction  
- Optimal decision timing  

---

## 🏆 Reward System

A **dense, multi-factor reward design**:

- Emotion Score → empathy handling  
- Decision Score → correctness  
- Efficiency Score → optimal steps  

✨ Features:
- Partial rewards  
- Penalties for premature actions  
- Bonus for optimal sequences  

**Ideal Strategy:**
```text
apologize → gather_info → act_now
````

---

## 🤖 Baseline Agent

A deterministic agent that:

* Handles emotions first
* Gathers missing information
* Acts only when confident

✅ Ensures reproducibility
✅ Provides a strong benchmark baseline

---

## 🔌 API Endpoints

| Method | Endpoint     | Description               |
| ------ | ------------ | ------------------------- |
| POST   | `/reset`     | Reset environment         |
| POST   | `/step`      | Take an action            |
| GET    | `/state`     | Get current state         |
| POST   | `/run-agent` | Run full autonomous agent |

👉 Try it here:
[https://practiceof-eadi-openenv.hf.space/docs](https://practiceof-eadi-openenv.hf.space/docs)

---

## 🐳 Docker Deployment

```bash
docker build -t eadi-openenv .
docker run -p 7860:7860 eadi-openenv
```

---

## 🧪 Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 7860
```

---

## 📊 Inference

```bash
python inference.py
```

Example output:

```
[START]
[STEP]
[END]
```

---

## 🧠 Key Innovations

* Emotion-aware RL environment
* Decision-making under uncertainty
* Multi-step reasoning evaluation
* Sequence-sensitive reward system
* Real-world simulation scenarios

---

## 🔮 Future Scope

* Dynamic emotion transitions
* Multi-agent collaboration
* Real-time streaming inputs
* Integration with LLM-based agents (Gemma, etc.)

---

## 🏁 Conclusion

EADI shifts the focus from:

> ❌ “Is the answer correct?”
> to
> ✅ “Was the decision **human-aware, timely, and intelligent**?”

---

## 👩‍💻 Author

**Sakshi Selmokar**
AI/ML Engineer

**Prajakta Hake**
AI/ML Engineer

---

⭐ If you found this interesting, consider starring the repo!

```
