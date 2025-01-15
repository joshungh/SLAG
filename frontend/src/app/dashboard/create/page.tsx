"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Wand2, Bell } from "lucide-react";
import { useWeb3 } from "@/contexts/Web3Context";
import { useAuth } from "@/contexts/AuthContext";
import GenerationProgress from "@/components/GenerationProgress";
import { useRouter } from "next/navigation";
import { useStoryQueue } from "@/contexts/StoryQueueContext";

export default function CreatePage() {
  const [prompt, setPrompt] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [showCursor, setShowCursor] = useState(true);
  const { connected } = useWeb3();
  const { user } = useAuth();
  const { queue, addToQueue } = useStoryQueue();
  const router = useRouter();

  interface Step {
    id: string;
    title: string;
    status: "pending" | "in-progress" | "completed";
  }

  const initialSteps: Step[] = [
    {
      id: "world-genesis",
      title: "World Building",
      status: "pending",
    },
    {
      id: "story-bible",
      title: "Story Bible",
      status: "pending",
    },
    {
      id: "outline",
      title: "Story Outline",
      status: "pending",
    },
    {
      id: "scene-drafts",
      title: "Scene Writing",
      status: "pending",
    },
    {
      id: "final-assembly",
      title: "Final Polish",
      status: "pending",
    },
  ];

  const isAuthenticated = connected || !!user;

  // Add logging to debug auth state
  useEffect(() => {
    console.log("Auth state:", { connected, user, isAuthenticated });
  }, [connected, user, isAuthenticated]);

  // Cursor blink effect with cleanup
  useEffect(() => {
    const interval = setInterval(() => {
      setShowCursor((prev) => !prev);
    }, 500);
    return () => clearInterval(interval);
  }, []);

  // Request notification permission
  useEffect(() => {
    if ("Notification" in window && Notification.permission === "default") {
      Notification.requestPermission();
    }
  }, []);

  const handleGenerate = async () => {
    if (!isAuthenticated) {
      setError("Please connect your wallet or sign in to generate stories");
      return;
    }

    if (!prompt.trim()) {
      setError("Please enter a story idea");
      return;
    }

    setError(null);
    addToQueue(prompt.trim());
    setPrompt(""); // Clear the prompt after adding to queue
  };

  // Get the current generating story if any
  const generatingStory = queue.find((task) => task.status === "generating");

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="container mx-auto px-4 py-8 sm:py-12 max-w-3xl"
    >
      <div className="space-y-8">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="text-center space-y-3"
        >
          <h1 className="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text text-transparent">
            Create Your Story
          </h1>
          <p className="text-gray-400 text-sm sm:text-base">
            Enter your story idea and let our AI bring it to life
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="space-y-4"
        >
          <div className="relative group">
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="w-full h-32 sm:h-40 px-4 py-3 rounded-xl bg-black/50 border border-gray-800 group-hover:border-green-500/50 focus:border-green-500 focus:ring-1 focus:ring-green-500 transition-all text-green-400 font-['IBM_Plex_Mono'] text-sm sm:text-base tracking-tight resize-none"
              disabled={false}
            />
            <div
              className="absolute pointer-events-none select-none"
              style={{
                top: "12px",
                left: "16px",
                right: "16px",
                opacity: prompt ? 0 : 1,
              }}
            >
              <span className="font-['IBM_Plex_Mono'] text-base sm:text-lg tracking-tight text-gray-500">
                Enter your story idea...
                <span
                  className={`text-green-400 ${
                    showCursor ? "opacity-100" : "opacity-0"
                  } transition-opacity`}
                >
                  ▋
                </span>
              </span>
            </div>
          </div>

          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-red-500/10 border border-red-500 text-red-400 text-sm p-3 rounded-lg"
            >
              {error}
            </motion.div>
          )}

          <motion.button
            onClick={handleGenerate}
            disabled={!prompt.trim()}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="w-full py-3 px-4 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 rounded-lg font-medium flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all text-white text-base shadow-lg shadow-green-500/20"
          >
            <Wand2 className="w-5 h-5" />
            <span>Generate Story</span>
          </motion.button>
        </motion.div>

        {/* Active Generation Progress */}
        {generatingStory && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <GenerationProgress
              steps={initialSteps}
              currentStepIndex={generatingStory.currentStep}
              overallProgress={generatingStory.progress}
            />
          </motion.div>
        )}

        {/* Story Queue */}
        {queue.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="bg-black/30 backdrop-blur-sm rounded-xl p-4 space-y-3"
          >
            <h2 className="text-sm font-medium text-gray-300 flex items-center gap-2">
              <Bell className="w-4 h-4" />
              Story Queue
            </h2>
            <div className="space-y-2">
              {queue.map((task) => (
                <div
                  key={task.id}
                  className="flex items-center justify-between py-2 px-3 rounded-lg bg-black/20 border border-gray-800"
                >
                  <div className="flex items-center space-x-2">
                    <div
                      className={`w-2 h-2 rounded-full ${
                        task.status === "generating"
                          ? "bg-blue-500 animate-pulse"
                          : task.status === "completed"
                          ? "bg-green-500"
                          : task.status === "error"
                          ? "bg-red-500"
                          : "bg-gray-500"
                      }`}
                    />
                    <span className="text-sm text-gray-400 truncate max-w-[300px] sm:max-w-[400px]">
                      {task.prompt}
                    </span>
                  </div>
                  <span className="text-xs text-gray-500 capitalize">
                    {task.status}
                  </span>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}
