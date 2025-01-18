"use client";

import { motion } from "framer-motion";

export function AnimatedEllipsis() {
  return (
    <span className="inline-flex items-center space-x-0.5 ml-1">
      <motion.span
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{
          repeat: Infinity,
          duration: 0.8,
          repeatType: "reverse",
          delay: 0,
        }}
        className="w-1 h-1 rounded-full bg-blue-400"
      />
      <motion.span
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{
          repeat: Infinity,
          duration: 0.8,
          repeatType: "reverse",
          delay: 0.2,
        }}
        className="w-1 h-1 rounded-full bg-blue-400"
      />
      <motion.span
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{
          repeat: Infinity,
          duration: 0.8,
          repeatType: "reverse",
          delay: 0.4,
        }}
        className="w-1 h-1 rounded-full bg-blue-400"
      />
    </span>
  );
}
