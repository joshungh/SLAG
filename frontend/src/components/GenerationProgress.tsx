"use client";

import { Clock, Sparkles } from "lucide-react";
import { motion } from "framer-motion";
import { useState, useEffect } from "react";

interface Step {
  id: string;
  title: string;
  status: "pending" | "in-progress" | "completed";
}

interface GenerationProgressProps {
  steps: Step[];
  currentStepIndex: number;
  overallProgress: number;
}

export default function GenerationProgress({
  steps,
  currentStepIndex,
  overallProgress,
}: GenerationProgressProps) {
  const [showParticles, setShowParticles] = useState(false);

  useEffect(() => {
    if (overallProgress === 100) {
      setShowParticles(true);
      const timeout = setTimeout(() => setShowParticles(false), 2000);
      return () => clearTimeout(timeout);
    }
  }, [overallProgress]);

  return (
    <div className="bg-black/30 backdrop-blur-sm rounded-xl p-4 space-y-6">
      {/* Overall Progress */}
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2">
            <span className="text-base font-medium text-gray-300">
              Progress
            </span>
            {showParticles && (
              <motion.div
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", stiffness: 400, damping: 10 }}
              >
                <Sparkles className="w-4 h-4 text-blue-400" />
              </motion.div>
            )}
          </div>
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4 text-gray-400" />
            <span className="text-sm font-medium text-gray-400">
              {overallProgress}%
            </span>
          </div>
        </div>

        {/* Progress Bar and Steps */}
        <div className="relative pt-8 pb-6">
          {/* Progress Bar */}
          <div className="relative">
            {/* Background Bar */}
            <div className="h-2 bg-gray-800/50 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500"
                initial={{ width: 0 }}
                animate={{ width: `${overallProgress}%` }}
                transition={{ duration: 0.5 }}
              />
            </div>

            {/* Step Dots and Labels */}
            <div className="absolute -top-1.5 left-0 right-0">
              <div className="relative h-12">
                {steps.map((step, index) => {
                  const isCompleted = index < currentStepIndex;
                  const isActive = index === currentStepIndex;
                  const position = (index / (steps.length - 1)) * 100;

                  return (
                    <div
                      key={step.id}
                      className="absolute transform -translate-x-1/2"
                      style={{ left: `${position}%` }}
                    >
                      {/* Dot */}
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ delay: index * 0.1 }}
                        className="flex justify-center"
                      >
                        <div
                          className={`w-4 h-4 rounded-full border-2 ${
                            isCompleted
                              ? "bg-blue-500 border-blue-500"
                              : isActive
                              ? "bg-purple-500 border-purple-500 animate-pulse"
                              : "bg-gray-800 border-gray-700"
                          } transition-colors`}
                        />
                      </motion.div>

                      {/* Label - Desktop Only */}
                      <div className="hidden sm:block absolute top-6 left-1/2 transform -translate-x-1/2 whitespace-nowrap">
                        <span
                          className="text-xs"
                          style={{
                            color: isCompleted
                              ? "#60A5FA"
                              : isActive
                              ? "#A855F7"
                              : "#6B7280",
                          }}
                        >
                          {step.title}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Current Step - Mobile Only */}
          <div className="sm:hidden text-center mt-6">
            <span
              className="text-sm"
              style={{
                color: "#A855F7",
              }}
            >
              {steps[currentStepIndex]?.title}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
