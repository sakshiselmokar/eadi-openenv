import { motion } from "framer-motion";

interface Props {
  currentReward: number;
  totalScore: number;
  quality: "Poor" | "Average" | "Good" | "Excellent";
  stepCount: number;
  totalSteps: number;
}

const qualityColors: Record<string, string> = {
  Poor: "text-destructive",
  Average: "emotion-confused",
  Good: "emotion-calm",
  Excellent: "emotion-satisfied",
};

export default function MetricsPanel({ currentReward, totalScore, quality, stepCount, totalSteps }: Props) {
  const progress = totalSteps > 0 ? (stepCount / totalSteps) * 100 : 0;

  return (
    <div className="glass-panel p-5">
      <h2 className="text-xs font-mono uppercase tracking-widest text-muted-foreground mb-4">Performance Metrics</h2>

      <div className="grid grid-cols-4 gap-4">
        {/* Current Reward */}
        <div className="text-center">
          <span className="text-[10px] font-mono text-muted-foreground uppercase">Last Reward</span>
          <motion.div
            key={currentReward}
            initial={{ scale: 1.3, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="text-2xl font-bold text-accent font-mono mt-1"
          >
            +{currentReward}
          </motion.div>
        </div>

        {/* Total Score */}
        <div className="text-center">
          <span className="text-[10px] font-mono text-muted-foreground uppercase">Total Score</span>
          <motion.div
            key={totalScore}
            initial={{ scale: 1.2 }}
            animate={{ scale: 1 }}
            className="text-2xl font-bold text-primary font-mono glow-text mt-1"
          >
            {totalScore}
          </motion.div>
        </div>

        {/* Quality */}
        <div className="text-center">
          <span className="text-[10px] font-mono text-muted-foreground uppercase">Quality</span>
          <div className={`text-2xl font-bold font-mono mt-1 ${qualityColors[quality]}`}>
            {quality}
          </div>
        </div>

        {/* Progress */}
        <div>
          <span className="text-[10px] font-mono text-muted-foreground uppercase">Progress</span>
          <div className="mt-2">
            <div className="h-2 rounded-full bg-secondary overflow-hidden">
              <motion.div
                className="h-full rounded-full bg-primary progress-glow"
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>
            <span className="text-[10px] font-mono text-muted-foreground mt-1 block text-right">
              {stepCount}/{totalSteps}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
