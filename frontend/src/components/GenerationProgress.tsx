"use client";

import { motion, AnimatePresence } from "framer-motion";
import {
  CheckCircle2,
  Loader2,
  AlertCircle,
  Clock,
  ChevronDown,
  ChevronUp,
  Sparkles,
  Brain,
} from "lucide-react";
import { useState, useEffect } from "react";

export interface LogMessage {
  timestamp: string;
  message: string;
  type: "info" | "warning" | "error";
}

export interface GenerationStep {
  id: string;
  title: string;
  description: string;
  status: "pending" | "in_progress" | "completed" | "error";
  progress?: number;
  estimatedTime?: string;
  logs?: LogMessage[];
}

interface GenerationProgressProps {
  steps: GenerationStep[];
  currentStepIndex: number;
  overallProgress: number;
}

const LoadingParticles = () => {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      <div className="absolute inset-0 flex items-center justify-center">
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-blue-400/30 rounded-full"
            animate={{
              scale: [1, 1.5, 1],
              opacity: [0.3, 0.8, 0.3],
              x: [
                Math.cos((i * (Math.PI * 2)) / 20) * 100,
                Math.cos(((i + 1) * (Math.PI * 2)) / 20) * 100,
              ],
              y: [
                Math.sin((i * (Math.PI * 2)) / 20) * 100,
                Math.sin(((i + 1) * (Math.PI * 2)) / 20) * 100,
              ],
            }}
            transition={{
              duration: 3,
              repeat: Infinity,
              delay: i * 0.1,
              ease: "linear",
            }}
          />
        ))}
      </div>
    </div>
  );
};

const TypingIndicator = () => {
  return (
    <div className="flex space-x-1">
      {[...Array(3)].map((_, i) => (
        <motion.div
          key={i}
          className="w-1 h-1 bg-blue-400 rounded-full"
          animate={{ scale: [1, 1.5, 1], opacity: [0.3, 1, 0.3] }}
          transition={{
            duration: 0.6,
            repeat: Infinity,
            delay: i * 0.2,
          }}
        />
      ))}
    </div>
  );
};

export default function GenerationProgress({
  steps,
  currentStepIndex,
  overallProgress,
}: GenerationProgressProps) {
  const [expandedSteps, setExpandedSteps] = useState<string[]>([]);
  const [showParticles, setShowParticles] = useState(false);

  useEffect(() => {
    // Show particles animation when there's an in-progress step
    const hasInProgressStep = steps.some(
      (step) => step.status === "in_progress"
    );
    setShowParticles(hasInProgressStep);
  }, [steps]);

  const toggleStep = (stepId: string) => {
    setExpandedSteps((prev) =>
      prev.includes(stepId)
        ? prev.filter((id) => id !== stepId)
        : [...prev, stepId]
    );
  };

  return (
    <div className="relative w-full max-w-2xl mx-auto bg-black/50 backdrop-blur-sm rounded-lg p-6 border border-white/10">
      {showParticles && <LoadingParticles />}

      {/* AI Processing Indicator */}
      {showParticles && (
        <div className="absolute -top-12 left-1/2 transform -translate-x-1/2 bg-blue-500/10 backdrop-blur-sm px-4 py-2 rounded-full border border-blue-400/20 flex items-center gap-2">
          <Brain className="w-4 h-4 text-blue-400" />
          <span className="text-sm text-blue-400">AI Processing</span>
          <TypingIndicator />
        </div>
      )}

      {/* Overall Progress */}
      <div className="mb-8 relative">
        <div className="flex justify-between items-center mb-2">
          <h3 className="text-lg font-medium flex items-center gap-2">
            Story Generation Progress
            {showParticles && <Sparkles className="w-4 h-4 text-blue-400" />}
          </h3>
          <div className="flex items-center space-x-2">
            <Clock className="w-4 h-4 text-gray-400" />
            <span className="text-sm text-gray-400">{overallProgress}%</span>
          </div>
        </div>
        <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500"
            initial={{ width: 0 }}
            animate={{ width: `${overallProgress}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>

      {/* Steps */}
      <div className="space-y-4">
        <AnimatePresence>
          {steps.map((step, index) => {
            const isExpanded = expandedSteps.includes(step.id);
            const hasLogs = step.logs && step.logs.length > 0;
            const isActive = index === currentStepIndex;

            return (
              <motion.div
                key={step.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className={`relative ${
                  isActive
                    ? "bg-gradient-to-r from-blue-500/5 to-transparent"
                    : ""
                } rounded-lg p-4 transition-colors border border-white/5 hover:border-white/10`}
              >
                {/* Active step indicator */}
                {isActive && step.status === "in_progress" && (
                  <motion.div
                    className="absolute inset-0 rounded-lg"
                    animate={{
                      boxShadow: [
                        "0 0 0 0 rgba(59, 130, 246, 0)",
                        "0 0 0 4px rgba(59, 130, 246, 0.1)",
                        "0 0 0 0 rgba(59, 130, 246, 0)",
                      ],
                    }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                      ease: "easeInOut",
                    }}
                  />
                )}

                <div className="flex items-start gap-4">
                  {/* Status Icon */}
                  <div className="mt-1">
                    <AnimatePresence mode="wait">
                      {step.status === "completed" ? (
                        <motion.div
                          key="completed"
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          exit={{ scale: 0 }}
                        >
                          <CheckCircle2 className="w-5 h-5 text-green-400" />
                        </motion.div>
                      ) : step.status === "in_progress" ? (
                        <motion.div
                          key="in_progress"
                          initial={{ rotate: 0 }}
                          animate={{ rotate: 360 }}
                          transition={{
                            duration: 2,
                            repeat: Infinity,
                            ease: "linear",
                          }}
                        >
                          <Loader2 className="w-5 h-5 text-blue-400" />
                        </motion.div>
                      ) : step.status === "error" ? (
                        <motion.div
                          key="error"
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          exit={{ scale: 0 }}
                        >
                          <AlertCircle className="w-5 h-5 text-red-400" />
                        </motion.div>
                      ) : (
                        <motion.div
                          key="pending"
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                          exit={{ scale: 0 }}
                        >
                          <div className="w-5 h-5 rounded-full border-2 border-gray-600" />
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>

                  {/* Step Content */}
                  <div className="flex-1">
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="font-medium flex items-center gap-2">
                          {step.title}
                          {hasLogs && (
                            <button
                              onClick={() => toggleStep(step.id)}
                              className="text-gray-400 hover:text-white transition-colors"
                            >
                              {isExpanded ? (
                                <ChevronUp className="w-4 h-4" />
                              ) : (
                                <ChevronDown className="w-4 h-4" />
                              )}
                            </button>
                          )}
                        </h4>
                        <p className="text-sm text-gray-400 mt-1">
                          {step.description}
                        </p>
                      </div>
                      {step.estimatedTime && step.status === "in_progress" && (
                        <motion.span
                          initial={{ opacity: 0, x: 20 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: -20 }}
                          className="text-xs text-gray-500 flex items-center space-x-1"
                        >
                          <Clock className="w-3 h-3" />
                          <span>~{step.estimatedTime} remaining</span>
                        </motion.span>
                      )}
                    </div>

                    {/* Step Progress (if available) */}
                    {step.progress !== undefined &&
                      step.status === "in_progress" && (
                        <motion.div
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: "auto" }}
                          exit={{ opacity: 0, height: 0 }}
                          className="mt-3"
                        >
                          <div className="h-1 bg-gray-800 rounded-full overflow-hidden">
                            <motion.div
                              className="h-full bg-gradient-to-r from-blue-400 to-blue-300"
                              initial={{ width: 0 }}
                              animate={{ width: `${step.progress}%` }}
                              transition={{ duration: 0.3 }}
                            />
                          </div>
                        </motion.div>
                      )}

                    {/* Logs Section */}
                    {hasLogs && isExpanded && step.logs && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: "auto" }}
                        exit={{ opacity: 0, height: 0 }}
                        className="mt-4 space-y-2"
                      >
                        <div className="bg-black/30 rounded-lg p-3 max-h-48 overflow-y-auto font-mono text-sm">
                          {step.logs.map((log, i) => (
                            <div
                              key={i}
                              className={`py-1 ${
                                log.type === "error"
                                  ? "text-red-400"
                                  : log.type === "warning"
                                  ? "text-yellow-400"
                                  : "text-gray-300"
                              }`}
                            >
                              <span className="text-gray-500">
                                {log.timestamp}
                              </span>{" "}
                              {log.message}
                            </div>
                          ))}
                        </div>
                      </motion.div>
                    )}
                  </div>
                </div>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </div>
    </div>
  );
}
