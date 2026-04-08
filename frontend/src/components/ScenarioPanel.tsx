import { motion, AnimatePresence } from "framer-motion";
import type { Emotion } from "@/hooks/useSimulation";

interface Props {
  message: string;
  emotion: Emotion;
  emoji: string;
  context: string;
}

const emotionLabels: Record<Emotion, string> = {
  angry: "Angry",
  confused: "Confused",
  calm: "Calm",
  satisfied: "Satisfied",
  neutral: "Neutral",
};

export default function ScenarioPanel({ message, emotion, emoji, context }: Props) {
  return (
    <div className="glass-panel p-6 h-full flex flex-col gap-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xs font-mono uppercase tracking-widest text-muted-foreground">Scenario Input</h2>
        {context && (
          <span className="text-[10px] font-mono px-2 py-1 rounded-full bg-primary/10 text-primary border border-primary/20">
            {context}
          </span>
        )}
      </div>

      <AnimatePresence mode="wait">
        {message ? (
          <motion.div
            key="msg"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex-1"
          >
            <p className="text-foreground text-sm leading-relaxed font-medium">
              "{message}"
            </p>
          </motion.div>
        ) : (
          <div className="flex-1 flex items-center justify-center text-muted-foreground text-sm">
            Awaiting scenario...
          </div>
        )}
      </AnimatePresence>

      {message && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className={`flex items-center gap-2 px-3 py-2 rounded-lg border bg-emotion-${emotion} w-fit`}
        >
          <span className="text-lg">{emoji}</span>
          <span className={`text-xs font-mono font-semibold emotion-${emotion}`}>
            {emotionLabels[emotion]}
          </span>
        </motion.div>
      )}
    </div>
  );
}
