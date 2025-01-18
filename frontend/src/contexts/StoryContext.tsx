"use client";

import React, {
  createContext,
  useContext,
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";
import { useAuth } from "./AuthContext";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL;

interface Story {
  id: string;
  user_id: string;
  title: string;
  content: string;
  genre: string;
  word_count: number;
  created_at: string;
  bible: {
    characters: any[];
    locations: any[];
    factions: any[];
    technology: any[];
    timeline: any[];
  };
  framework: {
    arcs: any[];
    beats: any[];
    themes: any[];
  };
}

interface StoryContextType {
  stories: Story[];
  setStories: (stories: Story[]) => void;
  deleteStory: (storyId: string) => Promise<void>;
  loading: boolean;
  error: string | null;
  refreshStories: () => Promise<void>;
}

const StoryContext = createContext<StoryContextType | undefined>(undefined);

export function StoryProvider({ children }: { children: React.ReactNode }) {
  const { user } = useAuth();
  const [stories, setStories] = useState<Story[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fetchInProgress = useRef(false);

  const fetchStories = useCallback(async () => {
    if (!user) {
      setStories([]);
      setLoading(false);
      return;
    }

    if (fetchInProgress.current) {
      return;
    }

    try {
      fetchInProgress.current = true;
      setLoading(true);
      const token = localStorage.getItem("auth_token");
      if (!token) {
        throw new Error("No auth token found");
      }

      const response = await fetch(`${BACKEND_URL}/api/stories`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch stories");
      }

      const data = await response.json();
      setStories(data.stories || []);
      setError(null);
    } catch (error) {
      setError(
        error instanceof Error ? error.message : "Failed to fetch stories"
      );
    } finally {
      setLoading(false);
      fetchInProgress.current = false;
    }
  }, [user]);

  const deleteStory = useCallback(async (storyId: string) => {
    if (!process.env.NEXT_PUBLIC_API_URL)
      throw new Error("API URL not configured");

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/stories/${storyId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
          },
        }
      );

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.message || `Failed to delete story (${response.status})`
        );
      }

      // Update local state after successful deletion
      setStories((prev) => prev.filter((story) => story.id !== storyId));
    } catch (error) {
      console.error("Error deleting story:", error);
      throw error;
    }
  }, []);

  return (
    <StoryContext.Provider
      value={{
        stories,
        setStories,
        deleteStory,
        loading,
        error,
        refreshStories: fetchStories,
      }}
    >
      {children}
    </StoryContext.Provider>
  );
}

export function useStories() {
  const context = useContext(StoryContext);
  if (context === undefined) {
    throw new Error("useStories must be used within a StoryProvider");
  }
  return context;
}

export type { Story };
