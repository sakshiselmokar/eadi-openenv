import { useState, useCallback, useRef } from "react";

export type Emotion = "angry" | "confused" | "calm" | "satisfied" | "neutral";

export interface SimulationStep {
  id: number;
  action: string;
  reasoning: string;
  reward: number;
  emotionBefore: Emotion;
  emotionAfter: Emotion;
  timestamp: number;
}

export interface SimulationState {
  scenario: {
    message: string;
    emotion: Emotion;
    context: string;
    emoji: string;
  };
  knownFacts: string[];
  unknowns: string[];
  timeLeft: number;
  totalTime: number;
  steps: SimulationStep[];
  currentReward: number;
  totalScore: number;
  quality: "Poor" | "Average" | "Good" | "Excellent";
  isRunning: boolean;
  isDone: boolean;
  currentReasoning: string;
}

const DEMO_SCENARIO = {
  message: "I've been waiting 3 weeks for my refund. This is completely unacceptable. I want to speak to someone who can actually help me NOW.",
  emotion: "angry" as Emotion,
  context: "E-Commerce Customer Support",
  emoji: "😡",
};

const DEMO_FACTS = ["Customer waited 3 weeks", "Refund not processed", "Customer is escalating"];
const DEMO_UNKNOWNS = ["Refund reason unclear", "Order details missing", "Payment method unknown"];

const DEMO_STEPS: Omit<SimulationStep, "timestamp">[] = [
  {
    id: 1,
    action: "Acknowledge & Empathize",
    reasoning: "User frustration is at peak → applying empathy-first strategy to de-escalate before problem-solving",
    reward: 15,
    emotionBefore: "angry",
    emotionAfter: "angry",
  },
  {
    id: 2,
    action: "Retrieve Order History",
    reasoning: "Need concrete data to resolve issue → querying backend systems while maintaining conversation flow",
    reward: 10,
    emotionBefore: "angry",
    emotionAfter: "confused",
  },
  {
    id: 3,
    action: "Identify Processing Delay",
    reasoning: "Root cause found: payment gateway timeout → preparing transparent explanation to build trust",
    reward: 20,
    emotionBefore: "confused",
    emotionAfter: "calm",
  },
  {
    id: 4,
    action: "Initiate Expedited Refund",
    reasoning: "Immediate action maximizes satisfaction → escalating to priority queue with 24h guarantee",
    reward: 30,
    emotionBefore: "calm",
    emotionAfter: "calm",
  },
  {
    id: 5,
    action: "Offer Compensation",
    reasoning: "Customer lifetime value is high → proactive goodwill gesture increases retention probability by 73%",
    reward: 25,
    emotionBefore: "calm",
    emotionAfter: "satisfied",
  },
];

const initialState: SimulationState = {
  scenario: { message: "", emotion: "neutral", context: "", emoji: "🤖" },
  knownFacts: [],
  unknowns: [],
  timeLeft: 30,
  totalTime: 30,
  steps: [],
  currentReward: 0,
  totalScore: 0,
  quality: "Poor",
  isRunning: false,
  isDone: false,
  currentReasoning: "",
};

function getQuality(score: number): SimulationState["quality"] {
  if (score >= 80) return "Excellent";
  if (score >= 50) return "Good";
  if (score >= 25) return "Average";
  return "Poor";
}

export function useSimulation() {
  const [state, setState] = useState<SimulationState>(initialState);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const stepIndexRef = useRef(0);
  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);

  const cleanup = useCallback(() => {
    if (intervalRef.current) clearInterval(intervalRef.current);
    if (timerRef.current) clearInterval(timerRef.current);
    intervalRef.current = null;
    timerRef.current = null;
  }, []);

  const start = useCallback(() => {
    cleanup();
    stepIndexRef.current = 0;

    // Phase 1: Show scenario
    setState({
      ...initialState,
      scenario: DEMO_SCENARIO,
      knownFacts: DEMO_FACTS,
      unknowns: DEMO_UNKNOWNS,
      isRunning: true,
      timeLeft: 30,
      totalTime: 30,
    });

    // Timer countdown
    timerRef.current = setInterval(() => {
      setState((prev) => {
        if (prev.timeLeft <= 1 || prev.isDone) {
          if (timerRef.current) clearInterval(timerRef.current);
          return { ...prev, timeLeft: Math.max(0, prev.timeLeft - 1) };
        }
        return { ...prev, timeLeft: prev.timeLeft - 1 };
      });
    }, 1000);

    // Phase 2: Steps every 2s
    setTimeout(() => {
      intervalRef.current = setInterval(() => {
        const idx = stepIndexRef.current;
        if (idx >= DEMO_STEPS.length) {
          cleanup();
          setState((prev) => ({ ...prev, isRunning: false, isDone: true, currentReasoning: "Decision sequence complete. All objectives achieved." }));
          return;
        }

        const step = { ...DEMO_STEPS[idx], timestamp: Date.now() };
        stepIndexRef.current++;

        setState((prev) => {
          const newScore = prev.totalScore + step.reward;
          return {
            ...prev,
            steps: [...prev.steps, step],
            currentReward: step.reward,
            totalScore: newScore,
            quality: getQuality(newScore),
            currentReasoning: step.reasoning,
            scenario: { ...prev.scenario, emotion: step.emotionAfter, emoji: getEmoji(step.emotionAfter) },
          };
        });
      }, 2000);
    }, 1500);
  }, [cleanup]);

  const reset = useCallback(() => {
    cleanup();
    setState(initialState);
  }, [cleanup]);

  return { state, start, reset };
}

function getEmoji(emotion: Emotion): string {
  const map: Record<Emotion, string> = {
    angry: "😡",
    confused: "😕",
    calm: "😌",
    satisfied: "😊",
    neutral: "🤖",
  };
  return map[emotion];
}
