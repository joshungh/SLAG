"use client";

import { useState, useEffect } from "react";
import {
  Search,
  BookOpen,
  ListFilter,
  Heart,
  Users,
  History,
  LogIn,
  Download,
  X,
} from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { useWeb3 } from "@/contexts/Web3Context";
import { motion } from "framer-motion";
import Link from "next/link";

interface Story {
  id: string;
  user_id: string;
  title: string;
  genre: string;
  content: string;
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

interface StoryModalProps {
  story: Story;
  onClose: () => void;
}

function StoryModal({ story, onClose }: StoryModalProps) {
  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  const downloadStory = () => {
    const element = document.createElement("a");
    const file = new Blob([story.content], { type: "text/plain" });
    element.href = URL.createObjectURL(file);
    element.download = `${story.title}.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div
      className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 overflow-y-auto"
      onClick={handleBackdropClick}
    >
      <div className="min-h-screen px-4 py-8" onClick={handleBackdropClick}>
        <div
          className="bg-gray-900 rounded-lg w-full max-w-4xl mx-auto"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="p-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h2 className="text-2xl font-bold mb-1">{story.title}</h2>
                <div className="flex items-center space-x-4 text-sm text-gray-400">
                  <span>{story.genre}</span>
                  <span>{story.word_count} words</span>
                  <span>{new Date(story.created_at).toLocaleDateString()}</span>
                </div>
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={downloadStory}
                  className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                >
                  <Download className="w-5 h-5" />
                </button>
                <button
                  onClick={onClose}
                  className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>
            <div className="prose prose-invert max-w-none">
              <div className="whitespace-pre-wrap">{story.content}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function LibraryPage() {
  const [stories, setStories] = useState<Story[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedStory, setSelectedStory] = useState<Story | null>(null);
  const { user } = useAuth();
  const { connected } = useWeb3();

  const isAuthenticated = connected || !!user;

  useEffect(() => {
    if (!isAuthenticated) return;

    const fetchStories = async () => {
      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_API_URL}/api/stories`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("auth_token")}`,
            },
          }
        );

        if (!response.ok) {
          throw new Error("Failed to fetch stories");
        }

        const data = await response.json();
        setStories(data.stories || []);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    };

    fetchStories();
  }, [isAuthenticated]);

  if (!isAuthenticated) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="container mx-auto px-4 py-16 max-w-2xl text-center"
      >
        <BookOpen className="w-16 h-16 mx-auto mb-6 text-green-500 opacity-50" />
        <h1 className="text-3xl font-bold mb-4 bg-gradient-to-r from-green-400 to-emerald-500 bg-clip-text text-transparent">
          Welcome to Your Story Library
        </h1>
        <p className="text-gray-400 mb-8">
          Sign in to view your collection of AI-generated stories
        </p>
        <Link
          href="/dashboard"
          className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 rounded-lg font-medium space-x-2 text-white shadow-lg shadow-green-500/20 transition-all"
        >
          <LogIn className="w-5 h-5" />
          <span>Sign In to Continue</span>
        </Link>
      </motion.div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-green-400">Loading stories...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-red-400">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black">
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="flex flex-col space-y-6">
          <h1 className="text-3xl font-bold text-white">My Stories</h1>

          {/* Stories List */}
          <div className="space-y-4">
            {stories.length === 0 ? (
              <div className="text-gray-400 text-center py-8">
                No stories found. Create your first story to get started!
              </div>
            ) : (
              stories.map((story) => (
                <div
                  key={story.id}
                  className="flex items-center justify-between p-6 bg-gray-900/50 rounded-lg hover:bg-gray-900/70"
                >
                  <div>
                    <h3 className="text-white text-xl font-medium mb-2">
                      {story.title}
                    </h3>
                    <div className="text-gray-400 space-x-4">
                      <span>{story.genre}</span>
                      <span>•</span>
                      <span>{story.word_count} words</span>
                      <span>•</span>
                      <span>
                        {new Date(story.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                  <button
                    onClick={() => setSelectedStory(story)}
                    className="px-4 py-2 bg-green-400 text-black rounded hover:bg-green-300"
                  >
                    Read Story
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {selectedStory && (
        <StoryModal
          story={selectedStory}
          onClose={() => setSelectedStory(null)}
        />
      )}
    </div>
  );
}
