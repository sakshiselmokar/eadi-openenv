import { motion, AnimatePresence } from "framer-motion";
import type { SimulationStep, Emotion } from "@/hooks/useSimulation";

interface Props {
  steps: SimulationStep[];
  isRunning: boolean;
  isDone: boolean;
}

const emotionColors: Record<Emotion, string> = {
  angry: "emotion-angry",
  confused: "emotion-confused",
  calm: "emotion-calm",
  satisfied: "emotion-satisfied",
  neutral: "emotion-neutral",
};

const emotionEmojis: Record<Emotion, string> = {
  angry: "😡",
  confused: "😕",
  calm: "😌",
  satisfied: "😊",
  neutral: "🤖",
};

export default function DecisionTimeline({ steps, isRunning, isDone }: Props) {
  return (
    <div className="glass-panel-accent p-6 h-full flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xs font-mono uppercase tracking-widest text-muted-foreground">Decision Timeline</h2>
        {isRunning && (
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-accent glow-dot animate-pulse-glow" />
            <span className="text-[10px] font-mono text-accent">PROCESSING</span>
          </div>
        )}
        {isDone && (
          <span className="text-[10px] font-mono text-emerald-400 px-2 py-0.5 rounded-full border border-emerald-400/20 bg-emerald-400/10">
            COMPLETE
          </span>
        )}
      </div>

      <div className="flex-1 overflow-y-auto space-y-0 relative">
        {/* Vertical line */}
        {steps.length > 0 && (
          <div className="absolute left-4 top-3 bottom-3 w-px bg-border" />
        )}

        <AnimatePresence>
          {steps.map((step, i) => (
            <motion.div
              key={step.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, ease: "easeOut" }}
              className="relative pl-10 pb-5"
            >
              {/* Node */}
              <div className={`absolute left-2.5 top-1 w-3 h-3 rounded-full border-2 border-primary bg-background z-10 ${i === steps.length - 1 && isRunning ? "glow-dot text-primary" : ""}`} />

              <div className="glass-panel p-4 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-mono text-muted-foreground">STEP {step.id}</span>
                    <span className="text-sm font-semibold text-foreground">{step.action}</span>
                  </div>
                  <span className="text-xs font-mono text-accent">+{step.reward}</span>
                </div>

                {/* Emotion transition */}
                <div className="flex items-center gap-2 text-xs">
                  <span className={emotionColors[step.emotionBefore]}>
                    {emotionEmojis[step.emotionBefore]}
                  </span>
                  <span className="text-muted-foreground">→</span>
                  <span className={emotionColors[step.emotionAfter]}>
                    {emotionEmojis[step.emotionAfter]}
                  </span>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {steps.length === 0 && !isRunning && (
          <div className="flex items-center justify-center h-full text-muted-foreground text-sm">
            Timeline will appear here...
          </div>
        )}

        {steps.length === 0 && isRunning && (
          <div className="flex items-center justify-center h-full">
            <div className="flex items-center gap-2 text-accent">
              <span className="w-2 h-2 rounded-full bg-accent animate-pulse-glow" />
              <span className="text-xs font-mono">Analyzing scenario...</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
