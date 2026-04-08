import { motion, AnimatePresence } from "framer-motion";

interface Props {
  reasoning: string;
  isRunning: boolean;
}

export default function ReasoningPanel({ reasoning, isRunning }: Props) {
  return (
    <div className="glass-panel p-5 h-full flex flex-col">
      <div className="flex items-center gap-2 mb-3">
        <h2 className="text-xs font-mono uppercase tracking-widest text-muted-foreground">AI Reasoning</h2>
        {isRunning && (
          <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse-glow" />
        )}
      </div>

      <AnimatePresence mode="wait">
        {reasoning ? (
          <motion.div
            key={reasoning}
            initial={{ opacity: 0, y: 5 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="flex-1 flex items-start"
          >
            <div className="flex gap-3">
              <span className="text-primary text-lg mt-0.5">🧠</span>
              <p className="text-sm text-secondary-foreground leading-relaxed font-mono">
                "{reasoning}"
              </p>
            </div>
          </motion.div>
        ) : (
          <div className="flex-1 flex items-center justify-center text-muted-foreground text-sm font-mono">
            Waiting for AI to reason...
          </div>
        )}
      </AnimatePresence>
    </div>
  );
}
