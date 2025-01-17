"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Wand2, Bell } from "lucide-react";
import { useWeb3 } from "@/contexts/Web3Context";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import { useStoryQueue } from "@/contexts/StoryQueueContext";
import { GENERATION_STEPS } from "@/constants/steps";
import StoryPrompt from "@/components/StoryPrompt";
import { StoryQueueItem } from "@/components/StoryQueueItem";
import ErrorMessage from "@/components/ErrorMessage";
import clsx from "clsx";

export default function CreatePage() {
  const [prompt, setPrompt] = useState("");
  const [error, setError] = useState<string | null>(null);
  const { connected } = useWeb3();
  const { user } = useAuth();
  const { queue, addToQueue, clearQueue, retryTask, stopTask } =
    useStoryQueue();
  const router = useRouter();

  const isAuthenticated = connected || !!user;
  const generatingCount = queue.filter(
    (task) => task.status === "generating"
  ).length;
  const isGenerationLimitReached = generatingCount >= 2;

  // Add logging to debug auth state
  useEffect(() => {
    console.log("Auth state:", { connected, user, isAuthenticated });
  }, [connected, user, isAuthenticated]);

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

    if (isGenerationLimitReached) {
      setError(
        "You can only generate 2 stories at a time. Please wait for current generations to complete."
      );
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
            {isGenerationLimitReached && (
              <span className="block text-yellow-500 mt-1">
                (Currently generating 2 stories - maximum limit reached)
              </span>
            )}
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="space-y-4"
        >
          <StoryPrompt value={prompt} onChange={setPrompt} />

          <ErrorMessage message={error} />

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

        {/* Story Queue */}
        {queue.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="bg-black/30 backdrop-blur-sm rounded-xl p-4 space-y-3"
          >
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-medium text-gray-300 flex items-center gap-2">
                <Bell className="w-4 h-4" />
                Story Queue
              </h2>
              <button
                onClick={clearQueue}
                className="text-xs text-red-400 hover:text-red-300 transition-colors"
              >
                Clear Queue
              </button>
            </div>
            <div className="space-y-2">
              {queue.map((task) => (
                <StoryQueueItem
                  key={task.id}
                  task={task}
                  onStop={task.status === "generating" ? stopTask : undefined}
                />
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}
