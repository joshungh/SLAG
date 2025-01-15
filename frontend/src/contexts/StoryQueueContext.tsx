"use client";

import React, {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
} from "react";
import { v4 as uuidv4 } from "uuid";
import { useRouter } from "next/navigation";
import { useAuth } from "./AuthContext";

interface StoryTask {
  id: string;
  prompt: string;
  status: "queued" | "generating" | "completed" | "error";
  progress: number;
  currentStep: number;
  error?: string;
  storyId?: string;
}

interface StoryQueueContextType {
  queue: StoryTask[];
  addToQueue: (prompt: string) => void;
  removeFromQueue: (id: string) => void;
  clearQueue: () => void;
}

const StoryQueueContext = createContext<StoryQueueContextType | undefined>(
  undefined
);

const QUEUE_STORAGE_KEY = "story_queue";
const COMPLETED_QUEUE_TIMEOUT = 1000 * 60 * 5; // 5 minutes

export function StoryQueueProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [queue, setQueue] = useState<StoryTask[]>([]);
  const router = useRouter();
  const { user } = useAuth();

  // Load queue from localStorage on mount
  useEffect(() => {
    const savedQueue = localStorage.getItem(QUEUE_STORAGE_KEY);
    if (savedQueue) {
      try {
        const parsedQueue = JSON.parse(savedQueue);
        // Only restore non-completed items that are less than 5 minutes old
        const now = Date.now();
        const filteredQueue = parsedQueue.filter(
          (task: StoryTask & { timestamp?: number }) => {
            if (task.status === "completed") {
              return (
                task.timestamp && now - task.timestamp < COMPLETED_QUEUE_TIMEOUT
              );
            }
            return true;
          }
        );
        setQueue(filteredQueue);
      } catch (error) {
        console.error("Error loading queue:", error);
      }
    }
  }, []);

  // Save queue to localStorage whenever it changes
  useEffect(() => {
    if (queue.length > 0) {
      // Add timestamp to completed items
      const queueWithTimestamps = queue.map((task) => {
        if (task.status === "completed" && !task.timestamp) {
          return { ...task, timestamp: Date.now() };
        }
        return task;
      });
      localStorage.setItem(
        QUEUE_STORAGE_KEY,
        JSON.stringify(queueWithTimestamps)
      );
    } else {
      localStorage.removeItem(QUEUE_STORAGE_KEY);
    }
  }, [queue]);

  // Process the next story in the queue
  const processNextStory = useCallback(async () => {
    // Find the first queued story
    const nextStory = queue.find((task) => task.status === "queued");
    if (!nextStory) return;

    // Update story status to generating
    setQueue((prev) =>
      prev.map((task) =>
        task.id === nextStory.id
          ? { ...task, status: "generating" as const }
          : task
      )
    );

    try {
      const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL;
      if (!BACKEND_URL) throw new Error("API URL not configured");

      // Call the test endpoint instead of the story engine
      const response = await fetch(`${BACKEND_URL}/api/stories/test`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
        },
      });

      if (!response.ok) throw new Error("Failed to generate story");

      const savedStory = await response.json();

      // Update queue with completed story
      setQueue((prev) =>
        prev.map((task) =>
          task.id === nextStory.id
            ? {
                ...task,
                status: "completed" as const,
                progress: 100,
                currentStep: 4,
                storyId: savedStory.id,
                timestamp: Date.now(),
              }
            : task
        )
      );

      // Show notification if supported
      if ("Notification" in window && Notification.permission === "granted") {
        new Notification("Story Generated!", {
          body: "Your story has been generated and saved to your library.",
          icon: "/favicon.ico",
        });
      }

      // Redirect to the library after a short delay
      setTimeout(() => {
        router.push("/dashboard/library");
      }, 2000);
    } catch (error) {
      console.error("Error processing story:", error);
      setQueue((prev) =>
        prev.map((task) =>
          task.id === nextStory.id
            ? {
                ...task,
                status: "error" as const,
                error: error instanceof Error ? error.message : "Unknown error",
              }
            : task
        )
      );
    }
  }, [queue, router]);

  // Process queue when it changes
  useEffect(() => {
    const hasGenerating = queue.some((task) => task.status === "generating");
    const hasQueued = queue.some((task) => task.status === "queued");

    if (!hasGenerating && hasQueued) {
      processNextStory();
    }
  }, [queue, processNextStory]);

  // Update progress for generating stories
  useEffect(() => {
    const generatingStory = queue.find((task) => task.status === "generating");
    if (!generatingStory) return;

    const interval = setInterval(() => {
      setQueue((prev) =>
        prev.map((task) => {
          if (task.id === generatingStory.id && task.status === "generating") {
            const newProgress = Math.min(task.progress + 5, 95);
            const stepIndex = Math.floor((newProgress / 95) * 4);
            return {
              ...task,
              progress: newProgress,
              currentStep: stepIndex,
            };
          }
          return task;
        })
      );
    }, 1000);

    return () => clearInterval(interval);
  }, [queue]);

  const addToQueue = useCallback((prompt: string) => {
    const newTask: StoryTask = {
      id: uuidv4(),
      prompt,
      status: "queued",
      progress: 0,
      currentStep: 0,
    };
    setQueue((prev) => [...prev, newTask]);
  }, []);

  const removeFromQueue = useCallback((id: string) => {
    setQueue((prev) => prev.filter((task) => task.id !== id));
  }, []);

  const clearQueue = useCallback(() => {
    setQueue([]);
    localStorage.removeItem(QUEUE_STORAGE_KEY);
  }, []);

  return (
    <StoryQueueContext.Provider
      value={{
        queue,
        addToQueue,
        removeFromQueue,
        clearQueue,
      }}
    >
      {children}
    </StoryQueueContext.Provider>
  );
}

export function useStoryQueue() {
  const context = useContext(StoryQueueContext);
  if (context === undefined) {
    throw new Error("useStoryQueue must be used within a StoryQueueProvider");
  }
  return context;
}
