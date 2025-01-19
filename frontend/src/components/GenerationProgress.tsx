"use client";

import { motion, AnimatePresence } from "framer-motion";
import { useEffect, useState } from "react";

interface GenerationProgressProps {
  currentStepIndex: number;
  overallProgress: number;
  wordCount?: number;
}

const progressMessages = [
  "Starting story generation process...",
  "Creating story world and characters...",
  "World building complete!",
  "Designing story framework...",
  "Story framework complete!",
  "Beginning story writing...",
];

export default function GenerationProgress({
  currentStepIndex,
  overallProgress,
  wordCount,
}: GenerationProgressProps) {
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);

  // Update message index based on progress
  useEffect(() => {
    if (overallProgress < 20) {
      setCurrentMessageIndex(0);
    } else if (overallProgress < 40) {
      setCurrentMessageIndex(1);
    } else if (overallProgress < 50) {
      setCurrentMessageIndex(2);
    } else if (overallProgress < 70) {
      setCurrentMessageIndex(3);
    } else if (overallProgress < 80) {
      setCurrentMessageIndex(4);
    } else if (overallProgress < 100) {
      setCurrentMessageIndex(5);
    }
  }, [overallProgress]);

  return (
    <div className="space-y-4">
      <AnimatePresence mode="wait">
        <motion.div
          key={currentMessageIndex}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.5 }}
          className="text-center text-gray-300 font-medium"
        >
          {overallProgress === 100 && wordCount
            ? `Story generation complete! Generated ${wordCount} words.`
            : progressMessages[currentMessageIndex]}
        </motion.div>
      </AnimatePresence>

      <div className="relative">
        <div className="overflow-hidden h-2 text-xs flex rounded-full bg-black/30 backdrop-blur-sm">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${overallProgress}%` }}
            transition={{ duration: 0.5 }}
            className="shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center bg-gradient-to-r from-green-400 to-emerald-500"
          />
        </div>
      </div>
    </div>
  );
}
