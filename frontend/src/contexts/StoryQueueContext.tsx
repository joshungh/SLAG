"use client";

import React, {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
  useRef,
} from "react";
import { v4 as uuidv4 } from "uuid";
import { useRouter } from "next/navigation";
import { useAuth } from "./AuthContext";

// Constants for queue management and timing
const QUEUE_STORAGE_KEY = "story_queue";
const COMPLETED_QUEUE_TIMEOUT = 1000 * 60 * 60; // 1 hour
const POLLING_INTERVAL = 1000 * 30; // Poll every 30 seconds
const REDIRECT_DELAY = 2000; // 2 seconds
const PROGRESS_UPDATE_INTERVAL = 1000; // 1 second
const PROGRESS_INCREMENT = 5;
const MAX_PROGRESS = 95;
const MAX_CONCURRENT_GENERATIONS = 2;

// Environment variables
const STORY_ENGINE_URL =
  process.env.NEXT_PUBLIC_STORY_ENGINE_URL ||
  "http://vmini-engine-alb-production-943444221.us-west-2.elb.amazonaws.com";
const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL;

// Story response interface
interface StoryContent {
  title: string;
  genre: string;
  content: string;
  word_count: number;
  bible: Record<string, unknown>;
  framework: Record<string, unknown>;
}

interface GenerateResponse {
  request_id: string;
  status: "queued";
}

interface StatusResponse {
  status: "queued" | "completed" | "failed";
  result?: {
    title: string;
    genre: string;
    content: string;
    created_at: string;
    word_count: number;
  };
}

/**
 * Represents a task in the story generation queue
 */
interface StoryTask {
  /** Unique identifier for the task */
  id: string;
  /** User's story prompt */
  prompt: string;
  /** Current status of the task */
  status: "generating" | "completed" | "error" | "stopped";
  /** Generation progress (0-100) */
  progress: number;
  /** Current step message in the generation process */
  currentStep: string;
  /** Error message if status is "error" */
  error?: string;
  /** ID of the generated story if completed */
  storyId?: string;
  /** Timestamp when the task was completed */
  timestamp?: number;
  /** Word count of the generated story */
  wordCount?: number;
  /** Request ID for the story generation */
  requestId?: string;
  /** Title of the completed story */
  title?: string;
}

/**
 * Context for managing the story generation queue
 */
interface StoryQueueContextType {
  /** Current queue of story tasks */
  queue: StoryTask[];
  /** Add a new story prompt to the queue */
  addToQueue: (prompt: string) => void;
  /** Remove a task from the queue by ID */
  removeFromQueue: (id: string) => void;
  /** Clear all tasks from the queue */
  clearQueue: () => void;
  /** Retry a failed task */
  retryTask: (id: string) => void;
  /** Stop a generating task */
  stopTask: (id: string) => void;
}

const StoryQueueContext = createContext<StoryQueueContextType | undefined>(
  undefined
);

// Add type for step progress
type StepProgress = {
  [key in "world" | "bible" | "outline" | "scenes" | "polish"]: {
    step: number;
    progress: number;
  };
};

const stepProgress: StepProgress = {
  world: { step: 0, progress: 20 },
  bible: { step: 1, progress: 40 },
  outline: { step: 2, progress: 60 },
  scenes: { step: 3, progress: 80 },
  polish: { step: 4, progress: 95 },
};

type StoryEngineStatus = keyof StepProgress | "completed" | "failed";

// Add type guard function
function isStepProgressKey(key: string): key is keyof StepProgress {
  return key in stepProgress;
}

interface User {
  user_id: string;
  // Add other user properties as needed
}

export function StoryQueueProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [queue, setQueue] = useState<StoryTask[]>([]);
  const [activePolls, setActivePolls] = useState<Record<string, boolean>>({});
  const router = useRouter();
  const { user } = useAuth() as { user: User | null };

  // Add request tracking
  const requestInProgress = useRef<boolean>(false);
  const isProcessingQueue = useRef<boolean>(false);
  const completedTasks = useRef<Set<string>>(new Set());

  // Helper function to handle errors - memoize with no dependencies
  const handleError = useCallback((taskId: string, error: unknown) => {
    setQueue((prev) =>
      prev.map((task) =>
        task.id === taskId
          ? {
              ...task,
              status: "error",
              error:
                error instanceof Error ? error.message : "An error occurred",
            }
          : task
      )
    );

    setActivePolls((prev) => {
      const newPolls = { ...prev };
      delete newPolls[taskId];
      return newPolls;
    });
  }, []); // No dependencies needed since it only uses setState functions

  // Helper function to handle story completion - depend only on handleError
  const handleCompletion = useCallback(
    async (taskId: string, data: any) => {
      try {
        // Skip if already completed
        if (completedTasks.current.has(taskId)) {
          return;
        }

        // Parse the result field which is a stringified JSON
        const storyData = JSON.parse(data.result);

        // Extract the needed fields from the parsed story data
        const storyToSave = {
          title: storyData.title,
          genre: storyData.genre,
          content: storyData.content,
          word_count: storyData.word_count,
          prompt: data.prompt,
          created_at: data.created_at,
          completed_at: data.completed_at,
          updated_at: data.updated_at,
          framework_id: storyData.framework_id,
          bible_id: storyData.bible_id,
          file_paths: storyData.file_paths,
        };

        // Save to backend DynamoDB
        const saveResponse = await fetch(`${BACKEND_URL}/api/stories`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
          },
          body: JSON.stringify(storyToSave),
        });

        if (!saveResponse.ok) {
          throw new Error("Failed to save completed story");
        }

        const savedStory = await saveResponse.json();

        completedTasks.current.add(taskId);

        // Update queue with completed story info and title
        setQueue((prev) =>
          prev.map((task) =>
            task.id === taskId
              ? {
                  ...task,
                  status: "completed",
                  progress: 100,
                  currentStep: "Story completed!",
                  storyId: savedStory.id,
                  timestamp: Date.now(),
                  wordCount: storyData.word_count,
                  title: storyData.title,
                }
              : task
          )
        );

        // Clean up stream
        setActivePolls((prev) => {
          const newPolls = { ...prev };
          delete newPolls[taskId];
          return newPolls;
        });
      } catch (error) {
        handleError(taskId, error);
      }
    },
    [handleError] // Only depend on handleError
  );

  // Process the stream data - depend only on handleCompletion and handleError
  const processStreamData = useCallback(
    (text: string, taskId: string, requestId: string) => {
      const line = text.trim();

      // Handle ping messages
      if (line.startsWith(": ping")) {
        return;
      }

      // Handle progress events
      if (line.startsWith("event: progress")) {
        return;
      }

      if (line.startsWith("data: ")) {
        const message = line.substring(6).trim();

        // Skip empty data lines
        if (!message || message === "data:") {
          return;
        }

        // Handle disconnect message
        if (message.includes("disconnect")) {
          return;
        }

        try {
          // Try to parse as JSON first
          const jsonData = JSON.parse(message);
          if (jsonData.complete) {
            // Skip if already completed
            if (completedTasks.current.has(taskId)) {
              return;
            }

            // For completion message, get the final data from the status endpoint
            fetch(`${STORY_ENGINE_URL}/status/${requestId}`, {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
              },
            })
              .then((response) => response.json())
              .then((data) => {
                if (data.status === "completed") {
                  void handleCompletion(taskId, data);
                }
              })
              .catch((error) => handleError(taskId, error));

            // Update UI
            setQueue((prev) =>
              prev.map((task) =>
                task.id === taskId
                  ? {
                      ...task,
                      currentStep: jsonData.message,
                      progress: 95,
                    }
                  : task
              )
            );
            return;
          }

          // Update with the message from JSON if available
          if (jsonData.message) {
            setQueue((prev) =>
              prev.map((task) =>
                task.id === taskId
                  ? {
                      ...task,
                      currentStep: jsonData.message,
                      progress: Math.min(task.progress + 10, 95),
                    }
                  : task
              )
            );
          }
        } catch {
          // If not JSON, treat as plain text
          if (message.trim()) {
            setQueue((prev) =>
              prev.map((task) =>
                task.id === taskId
                  ? {
                      ...task,
                      currentStep: message,
                      progress: Math.min(task.progress + 10, 95),
                    }
                  : task
              )
            );
          }
        }
      }
    },
    [handleCompletion, handleError] // Only depend on stable callbacks
  );

  // Helper function to start streaming - depend only on processStreamData and handleError
  const startStreaming = useCallback(
    (taskId: string, requestId: string) => {
      const startStream = async () => {
        try {
          const response = await fetch(
            `${STORY_ENGINE_URL}/stream/${requestId}`,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
              },
            }
          );

          if (!response.ok) {
            throw new Error(`Failed to connect to stream (${response.status})`);
          }

          const reader = response.body?.getReader();
          if (!reader) {
            throw new Error("Stream reader not available");
          }

          // Read the stream
          const decoder = new TextDecoder();
          let buffer = "";

          while (true) {
            const { done, value } = await reader.read();

            if (done) {
              break;
            }

            // Decode the chunk and add to buffer
            const chunk = decoder.decode(value, { stream: true });
            buffer += chunk;

            // Process complete lines
            const lines = buffer.split("\n");
            buffer = lines.pop() || ""; // Keep the incomplete line in the buffer

            // Process each complete line
            for (const line of lines) {
              if (line.trim()) {
                processStreamData(line, taskId, requestId);
              }
            }
          }
        } catch (error) {
          handleError(taskId, error);
        }
      };

      // Start the stream
      void startStream();
    },
    [processStreamData, handleError] // Only depend on stable callbacks
  );

  // Load queue from localStorage and restore streaming for generating stories
  useEffect(() => {
    if (!user) {
      setQueue([]);
      return;
    }

    const key = `${QUEUE_STORAGE_KEY}_${user.user_id}`;
    const savedQueue = localStorage.getItem(key);

    if (savedQueue) {
      try {
        const parsedQueue = JSON.parse(savedQueue);
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

        // Only update if queue is different
        setQueue((prevQueue) => {
          if (JSON.stringify(prevQueue) === JSON.stringify(filteredQueue)) {
            return prevQueue;
          }
          return filteredQueue;
        });

        // Reconnect to streams for any generating stories
        filteredQueue.forEach((task: StoryTask) => {
          if (task.status === "generating" && task.requestId) {
            startStreaming(task.id, task.requestId);
          }
        });
      } catch (error) {
        handleError("queue", error);
      }
    } else {
      setQueue([]);
    }
  }, [user?.user_id, startStreaming, handleError]); // Only depend on user ID, not the entire user object

  // Save queue to localStorage whenever it changes
  useEffect(() => {
    const saveQueue = () => {
      if (!user?.user_id) {
        return;
      }

      const key = `${QUEUE_STORAGE_KEY}_${user.user_id}`;
      if (queue.length > 0) {
        const queueWithTimestamps = queue.map((task) => {
          if (task.status === "completed" && !task.timestamp) {
            return { ...task, timestamp: Date.now() };
          }
          return task;
        });

        // Only save if the queue has actually changed
        const currentSaved = localStorage.getItem(key);
        const newValue = JSON.stringify(queueWithTimestamps);
        if (currentSaved !== newValue) {
          localStorage.setItem(key, newValue);
        }
      } else {
        localStorage.removeItem(key);
      }
    };

    // Debounce the save operation
    const timeoutId = setTimeout(saveQueue, 100);
    return () => clearTimeout(timeoutId);
  }, [queue, user?.user_id]); // Only depend on queue and user ID

  // Process the next story in the queue
  const processNextStory = useCallback(
    async (prompt: string, taskId: string) => {
      // Check if a request is already in progress
      if (requestInProgress.current) {
        return;
      }

      try {
        // Set request flag
        requestInProgress.current = true;

        // Initial POST to get request_id
        const response = await fetch(`${STORY_ENGINE_URL}/generate`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
          },
          body: JSON.stringify({ prompt }),
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(
            errorData.message ||
              `Failed to start story generation (${response.status})`
          );
        }

        const data = (await response.json()) as GenerateResponse;
        if (!data.request_id) {
          throw new Error("No request ID received from story engine");
        }

        const request_id = data.request_id;
        console.log("Story generation initiated with request ID:", request_id);

        // Update task with request ID and set to generating
        setQueue((prev) =>
          prev.map((task) =>
            task.id === taskId
              ? {
                  ...task,
                  requestId: request_id,
                  status: "generating" as const,
                  progress: 0,
                  currentStep: "", // Empty initial step, will be filled by stream
                }
              : task
          )
        );

        // Start streaming for this task
        startStreaming(taskId, request_id);

        // Reset request flag
        requestInProgress.current = false;
      } catch (error) {
        // Reset request flag
        requestInProgress.current = false;
        console.error("Story processing error occurred:", error);
        handleError(taskId, error);
      }
    },
    [startStreaming, handleError] // Only depend on stable callbacks
  );

  const addToQueue = useCallback(
    async (prompt: string) => {
      // Create new task with default message
      const newTask: StoryTask = {
        id: uuidv4(),
        prompt,
        status: "generating",
        progress: 0,
        currentStep: "Starting world generation...", // Default message that matches first stream message
      };

      // Add the task to the list first
      setQueue((prev) => {
        // Check if we're already at the limit
        const generatingCount = prev.filter(
          (task) => task.status === "generating"
        ).length;

        if (generatingCount >= MAX_CONCURRENT_GENERATIONS) {
          throw new Error(
            "Maximum number of concurrent generations reached. Please wait for current stories to complete."
          );
        }

        return [...prev, newTask];
      });

      // Process the story using processNextStory
      await processNextStory(prompt, newTask.id);
    },
    [processNextStory] // Only depend on the stable processNextStory callback
  );

  const removeFromQueue = useCallback((id: string) => {
    setQueue((prev) => prev.filter((task) => task.id !== id));
    // Remove from completed tasks when removing from queue
    completedTasks.current.delete(id);
  }, []);

  const clearQueue = useCallback(() => {
    setQueue([]);
    localStorage.removeItem(QUEUE_STORAGE_KEY);
    // Clear completed tasks when clearing queue
    completedTasks.current.clear();
  }, []);

  const retryTask = useCallback(
    async (id: string) => {
      // Get the task to retry
      const taskToRetry = queue.find((task) => task.id === id);
      if (!taskToRetry) return;

      // Check if we're at the generation limit
      const generatingCount = queue.filter(
        (task) => task.status === "generating"
      ).length;

      if (generatingCount >= MAX_CONCURRENT_GENERATIONS) {
        throw new Error(
          "Maximum number of concurrent generations reached. Please wait for current stories to complete."
        );
      }

      // Start generation immediately
      try {
        const response = await fetch(`${STORY_ENGINE_URL}/generate`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
          },
          body: JSON.stringify({ prompt: taskToRetry.prompt }),
        });

        if (!response.ok) {
          throw new Error("Failed to start story generation");
        }

        const data = (await response.json()) as GenerateResponse;
        if (!data.request_id) {
          throw new Error("No request ID received from story engine");
        }

        // Update task with new request ID and reset status
        setQueue((prev) =>
          prev.map((task) =>
            task.id === id
              ? {
                  ...task,
                  status: "generating" as const,
                  progress: 0,
                  currentStep: "Starting story generation...",
                  error: undefined,
                  requestId: data.request_id,
                }
              : task
          )
        );

        // Start streaming for this task
        startStreaming(id, data.request_id);
      } catch (error) {
        setQueue((prev) =>
          prev.map((task) =>
            task.id === id
              ? {
                  ...task,
                  status: "error" as const,
                  error:
                    error instanceof Error
                      ? error.message
                      : "Failed to start generation",
                }
              : task
          )
        );
      }
    },
    [queue, startStreaming]
  );

  const stopTask = useCallback((id: string) => {
    // Stop polling for this task
    setActivePolls((prev) => {
      const newPolls = { ...prev };
      delete newPolls[id];
      return newPolls;
    });

    // Update task status
    setQueue((prev) =>
      prev.map((task) =>
        task.id === id
          ? {
              ...task,
              status: "stopped",
              error: "Story generation stopped by user",
            }
          : task
      )
    );
  }, []);

  return (
    <StoryQueueContext.Provider
      value={{
        queue,
        addToQueue,
        removeFromQueue,
        clearQueue,
        retryTask,
        stopTask,
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
