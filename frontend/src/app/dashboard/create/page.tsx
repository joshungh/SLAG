"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Wand2 } from "lucide-react";
import { useWeb3 } from "@/contexts/Web3Context";
import GenerationProgress from "@/components/GenerationProgress";
import { useAuth } from "@/contexts/AuthContext";

export default function CreatePage() {
  const [prompt, setPrompt] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showCursor, setShowCursor] = useState(true);
  const [generatedStory, setGeneratedStory] = useState<any>(null);
  const { connected } = useWeb3();
  const { user } = useAuth();

  const isAuthenticated = connected || !!user;
  console.log("Auth state:", { connected, user, isAuthenticated });

  // Cursor blink effect
  useEffect(() => {
    const interval = setInterval(() => {
      setShowCursor((prev) => !prev);
    }, 500);
    return () => clearInterval(interval);
  }, []);

  // Generation steps simulation
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [overallProgress, setOverallProgress] = useState(0);
  const steps = [
    "Analyzing prompt...",
    "Building story bible...",
    "Generating characters...",
    "Creating plot outline...",
    "Writing story...",
  ];

  const startGeneration = async () => {
    if (!prompt.trim()) {
      setError("Please enter a story idea");
      return;
    }

    setError(null);
    setIsGenerating(true);
    setCurrentStepIndex(0);
    setOverallProgress(0);

    try {
      const response = await fetch("/api/story/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        throw new Error("Failed to generate story");
      }

      const data = await response.json();
      setGeneratedStory(data);
    } catch (err) {
      setError("Failed to generate story. Please try again.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-4 sm:py-8">
      <div className="max-w-2xl mx-auto space-y-6 sm:space-y-8">
        <div className="text-center space-y-3 sm:space-y-4">
          <h1 className="text-3xl sm:text-4xl font-bold">Create Your Story</h1>
        </div>

        <div className="space-y-3 sm:space-y-4">
          <div className="relative">
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="w-full h-24 sm:h-32 px-3 sm:px-4 py-2 sm:py-3 rounded-lg bg-black/50 border border-gray-700 focus:border-green-500 focus:ring-1 focus:ring-green-500 transition-colors text-green-400 font-['IBM_Plex_Mono'] text-sm sm:text-base tracking-tight"
              disabled={isGenerating || !isAuthenticated}
            />
            <div
              className="absolute pointer-events-none select-none"
              style={{
                top: "8px",
                left: "12px",
                right: "12px",
                opacity: prompt ? 0 : 1,
              }}
            >
              <span className="font-['IBM_Plex_Mono'] text-base sm:text-lg tracking-tight text-gray-500">
                Enter your story idea...
                <span
                  className={`text-green-400 ${
                    showCursor ? "opacity-100" : "opacity-0"
                  }`}
                >
                  ▋
                </span>
              </span>
            </div>
          </div>

          {error && (
            <div className="bg-red-500/10 border border-red-500 text-red-400 text-xs sm:text-sm p-2 sm:p-3 rounded-lg">
              {error}
            </div>
          )}

          <div className="relative group">
            <button
              onClick={startGeneration}
              disabled={isGenerating || !isAuthenticated}
              className="w-full py-2 sm:py-3 px-3 sm:px-4 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 rounded-lg font-medium flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-white text-sm sm:text-base"
            >
              <Wand2 className="w-4 h-4 sm:w-5 sm:h-5" />
              <span>{isGenerating ? "Generating..." : "Generate Story"}</span>
            </button>
            {!isAuthenticated && (
              <div className="absolute -top-10 sm:-top-12 left-1/2 -translate-x-1/2 w-max opacity-0 group-hover:opacity-100 transition-opacity bg-black/90 text-white text-xs sm:text-sm py-1.5 sm:py-2 px-2 sm:px-3 rounded pointer-events-none">
                You'll need to sign up for a free account
              </div>
            )}
          </div>
        </div>

        {isGenerating && (
          <GenerationProgress
            steps={steps.map((step) => ({
              id: step.toLowerCase().replace(/\s+/g, "-"),
              title: step,
              description: "",
              status: "pending",
              estimatedTime: "30s",
            }))}
            currentStepIndex={currentStepIndex}
            overallProgress={overallProgress}
          />
        )}

        {generatedStory && !isGenerating && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-black/50 rounded-lg p-4 sm:p-6 space-y-6 sm:space-y-8"
          >
            {/* Story content sections */}
            {/* ... rest of the story display code ... */}
          </motion.div>
        )}
      </div>
    </div>
  );
}