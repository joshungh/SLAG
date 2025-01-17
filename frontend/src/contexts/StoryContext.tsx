"use client";

import React, { createContext, useContext, useCallback } from "react";
import { useAuth } from "./AuthContext";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL;

interface Story {
  id: string;
  title: string;
  content: string;
  genre: string;
  word_count: number;
  created_at: string;
}

interface StoryContextType {
  deleteStory: (storyId: string) => Promise<void>;
}

const StoryContext = createContext<StoryContextType | undefined>(undefined);

export function StoryProvider({ children }: { children: React.ReactNode }) {
  const { user } = useAuth();

  const deleteStory = useCallback(async (storyId: string) => {
    if (!BACKEND_URL) throw new Error("API URL not configured");

    try {
      const response = await fetch(`${BACKEND_URL}/api/stories/${storyId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.message || `Failed to delete story (${response.status})`
        );
      }
    } catch (error) {
      console.error("Error deleting story:", error);
      throw error;
    }
  }, []);

  return (
    <StoryContext.Provider
      value={{
        deleteStory,
      }}
    >
      {children}
    </StoryContext.Provider>
  );
}

export function useStory() {
  const context = useContext(StoryContext);
  if (context === undefined) {
    throw new Error("useStory must be used within a StoryProvider");
  }
  return context;
}

export type { Story };
