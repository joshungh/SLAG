"use client";

import { motion } from "framer-motion";
import { StoryTask } from "@/contexts/StoryQueueContext";
import { Progress } from "./ui/progress";

interface StoryQueueItemProps {
  task: StoryTask;
  onStop?: (id: string) => void;
}

function AnimatedEllipsis() {
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

export function StoryQueueItem({ task, onStop }: StoryQueueItemProps) {
  const getStatusMessage = () => {
    switch (task.status) {
      case "generating":
        return task.currentStep || "";
      case "queued":
        return "Waiting to start...";
      case "completed":
        return "Story completed!";
      case "error":
        return task.error || "An error occurred";
      case "stopped":
        return "Story generation stopped";
      default:
        return "";
    }
  };

  return (
    <div className="flex flex-col space-y-2 py-2 px-3 rounded-lg bg-black/20 border border-gray-800">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <div
            className={`w-2 h-2 rounded-full ${
              task.status === "generating"
                ? "bg-blue-500 animate-pulse"
                : task.status === "completed"
                ? "bg-green-500"
                : task.status === "error" || task.status === "stopped"
                ? "bg-red-500"
                : "bg-gray-500"
            }`}
          />
          <span className="text-sm text-gray-400 truncate max-w-[300px] sm:max-w-[400px]">
            {task.prompt}
          </span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="flex items-center">
            <span className="text-xs text-gray-500 capitalize">
              {task.status === "generating" ? (
                <>
                  generating
                  <AnimatedEllipsis />
                </>
              ) : (
                task.status
              )}
            </span>
          </div>
          {task.status === "generating" && onStop && (
            <button
              onClick={() => onStop(task.id)}
              className="text-xs text-red-400 hover:text-red-300 transition-colors px-2 py-1 rounded-md hover:bg-red-400/10"
            >
              Stop
            </button>
          )}
        </div>
      </div>

      {task.status === "generating" && (
        <div className="px-4 space-y-1">
          <Progress value={task.progress} className="h-1" />
          <p className="text-xs text-gray-500">{getStatusMessage()}</p>
        </div>
      )}

      {task.status === "error" && (
        <div className="flex items-center justify-between px-2">
          <span className="text-xs text-red-400">{task.error}</span>
        </div>
      )}
    </div>
  );
}
