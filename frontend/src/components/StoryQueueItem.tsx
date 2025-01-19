"use client";

import { useRouter } from "next/navigation";
import { AnimatedEllipsis } from "./AnimatedEllipsis";
import { Progress } from "./ui/progress";

interface StoryQueueItemProps {
  task: {
    id: string;
    prompt: string;
    status: "generating" | "completed" | "error" | "stopped";
    progress: number;
    currentStep: string;
    error?: string;
    title?: string;
  };
  onStop?: (id: string) => void;
}

export function StoryQueueItem({ task, onStop }: StoryQueueItemProps) {
  const router = useRouter();

  const getStatusMessage = () => {
    switch (task.status) {
      case "generating":
        return task.currentStep || "";
      case "queued":
        return "Waiting to start...";
      case "completed":
        return task.title || "Story completed!";
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
          {task.status === "completed" && (
            <button
              onClick={() => router.push("/dashboard/library")}
              className="text-xs text-emerald-400 hover:text-emerald-300 transition-colors px-2 py-1 rounded-md hover:bg-emerald-400/10"
            >
              View in Library
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

      {task.status === "completed" && task.title && (
        <div className="px-4">
          <p className="text-sm text-emerald-400 font-medium">{task.title}</p>
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
