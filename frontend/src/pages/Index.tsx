import { motion } from "framer-motion";
import { useSimulation } from "@/hooks/useSimulation";
import ScenarioPanel from "@/components/ScenarioPanel";
import StatePanel from "@/components/StatePanel";
import DecisionTimeline from "@/components/DecisionTimeline";
import MetricsPanel from "@/components/MetricsPanel";
import ReasoningPanel from "@/components/ReasoningPanel";

const TOTAL_STEPS = 5;

export default function Index() {
  const { state, start, reset } = useSimulation();

  return (
    <div className="min-h-screen bg-background p-4 md:p-6 flex flex-col gap-4 font-display">
      {/* Header */}
      <header className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-primary/20 border border-primary/30 flex items-center justify-center">
            <span className="text-primary text-sm font-bold">E</span>
          </div>
          <div>
            <h1 className="text-sm font-bold text-foreground tracking-tight">EADI</h1>
            <p className="text-[10px] font-mono text-muted-foreground">Emotion-Aware Decision Intelligence</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {!state.isRunning && !state.isDone && (
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={start}
              className="px-5 py-2 rounded-lg bg-primary text-primary-foreground text-sm font-semibold font-mono shadow-lg shadow-primary/25 hover:shadow-primary/40 transition-shadow"
            >
              ▶ Start Scenario
            </motion.button>
          )}
          {state.isDone && (
            <motion.button
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => { reset(); setTimeout(start, 100); }}
              className="px-5 py-2 rounded-lg bg-secondary text-secondary-foreground text-sm font-semibold font-mono border border-border hover:bg-secondary/80 transition-colors"
            >
              ↻ Run Again
            </motion.button>
          )}
          {state.isRunning && (
            <div className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary/10 border border-primary/20">
              <span className="w-2 h-2 rounded-full bg-primary animate-pulse-glow" />
              <span className="text-xs font-mono text-primary">LIVE</span>
            </div>
          )}
        </div>
      </header>

      {/* Main Grid */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-4 min-h-0">
        {/* Left column: Scenario + Reasoning */}
        <div className="flex flex-col gap-4">
          <div className="flex-1">
            <ScenarioPanel
              message={state.scenario.message}
              emotion={state.scenario.emotion}
              emoji={state.scenario.emoji}
              context={state.scenario.context}
            />
          </div>
          <div className="flex-1">
            <ReasoningPanel
              reasoning={state.currentReasoning}
              isRunning={state.isRunning}
            />
          </div>
        </div>

        {/* Center: Timeline */}
        <div className="lg:col-span-1">
          <DecisionTimeline
            steps={state.steps}
            isRunning={state.isRunning}
            isDone={state.isDone}
          />
        </div>

        {/* Right: State */}
        <div>
          <StatePanel
            knownFacts={state.knownFacts}
            unknowns={state.unknowns}
            timeLeft={state.timeLeft}
            totalTime={state.totalTime}
            isRunning={state.isRunning}
          />
        </div>
      </div>

      {/* Bottom: Metrics */}
      <MetricsPanel
        currentReward={state.currentReward}
        totalScore={state.totalScore}
        quality={state.quality}
        stepCount={state.steps.length}
        totalSteps={TOTAL_STEPS}
      />
    </div>
  );
}
