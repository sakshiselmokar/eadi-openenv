import { motion } from "framer-motion";

interface Props {
  knownFacts: string[];
  unknowns: string[];
  timeLeft: number;
  totalTime: number;
  isRunning: boolean;
}

export default function StatePanel({ knownFacts, unknowns, timeLeft, totalTime, isRunning }: Props) {
  const pct = totalTime > 0 ? (timeLeft / totalTime) * 100 : 100;
  const urgent = timeLeft <= 10 && isRunning;

  return (
    <div className="glass-panel p-6 h-full flex flex-col gap-4">
      <h2 className="text-xs font-mono uppercase tracking-widest text-muted-foreground">Agent State</h2>

      <div className="space-y-3 flex-1">
        <div>
          <span className="text-[10px] font-mono text-muted-foreground uppercase tracking-wider">Known Facts</span>
          <div className="flex flex-wrap gap-1.5 mt-1.5">
            {knownFacts.length > 0 ? knownFacts.map((f, i) => (
              <motion.span
                key={f}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.1 }}
                className="text-[10px] font-mono px-2 py-1 rounded-md bg-accent/10 text-accent border border-accent/20"
              >
                {f}
              </motion.span>
            )) : (
              <span className="text-[10px] text-muted-foreground">—</span>
            )}
          </div>
        </div>

        <div>
          <span className="text-[10px] font-mono text-muted-foreground uppercase tracking-wider">Unknowns</span>
          <div className="flex flex-wrap gap-1.5 mt-1.5">
            {unknowns.length > 0 ? unknowns.map((u, i) => (
              <motion.span
                key={u}
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.1 + 0.3 }}
                className="text-[10px] font-mono px-2 py-1 rounded-md bg-destructive/10 text-destructive border border-destructive/20"
              >
                ? {u}
              </motion.span>
            )) : (
              <span className="text-[10px] text-muted-foreground">—</span>
            )}
          </div>
        </div>
      </div>

      {/* Timer */}
      <div>
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-[10px] font-mono text-muted-foreground uppercase tracking-wider">Time Remaining</span>
          <span className={`text-sm font-mono font-bold ${urgent ? "text-destructive animate-pulse" : "text-foreground"}`}>
            {timeLeft}s
          </span>
        </div>
        <div className="h-1.5 rounded-full bg-secondary overflow-hidden">
          <motion.div
            className={`h-full rounded-full ${urgent ? "bg-destructive" : "bg-primary"} progress-glow`}
            animate={{ width: `${pct}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>
    </div>
  );
}
