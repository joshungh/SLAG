"use client";

import { useState, useEffect, useCallback, useMemo, useRef } from "react";
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
  Globe,
  Clock,
  MoreVertical,
  Share2,
  Trash2,
} from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { useWeb3 } from "@/contexts/Web3Context";
import { motion } from "framer-motion";
import Link from "next/link";
import { DeleteStoryButton } from "@/components/DeleteStoryButton";
import { StoryProvider } from "@/contexts/StoryContext";
import { createPortal } from "react-dom";
import { useStories } from "@/contexts/StoryContext";

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
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        onClose();
      }
    };
    document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }, [onClose]);

  const downloadStory = () => {
    const element = document.createElement("a");
    const file = new Blob([story.content], { type: "text/plain" });
    element.href = URL.createObjectURL(file);
    element.download = `${story.title}.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return createPortal(
    <div className="fixed inset-0 bg-black/90 backdrop-blur-sm z-50 overflow-y-auto">
      <div className="min-h-screen px-4 py-8">
        <div className="modal-content bg-gradient-to-br from-gray-900 to-black border border-gray-800/50 rounded-xl w-full max-w-4xl mx-auto shadow-xl">
          <div className="border-b border-gray-800/50">
            <div className="p-6">
              <div className="flex items-start justify-between">
                <div>
                  <h2 className="text-2xl font-bold text-white mb-2">
                    {story.title}
                  </h2>
                  <div className="flex items-center gap-4 text-sm text-gray-400">
                    <div className="flex items-center gap-1.5">
                      <BookOpen className="w-4 h-4" />
                      <span>{story.genre}</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <Clock className="w-4 h-4" />
                      <span>
                        {new Date(story.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <BookOpen className="w-4 h-4" />
                      <span>{story.word_count} words</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={downloadStory}
                    className="p-2 hover:bg-white/10 rounded-lg transition-colors text-gray-400 hover:text-white"
                  >
                    <Download className="w-5 h-5" />
                  </button>
                  <button
                    onClick={onClose}
                    className="p-2 hover:bg-white/10 rounded-lg transition-colors text-gray-400 hover:text-white"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="p-6">
            <div className="prose prose-invert prose-green max-w-none">
              <div className="whitespace-pre-wrap leading-relaxed">
                {story.content}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>,
    document.body
  );
}

interface StoryDropdownProps {
  story: Story;
  isOpen: boolean;
  onClose: () => void;
  buttonRef: React.MutableRefObject<HTMLButtonElement | null>;
}

function StoryDropdown({
  story,
  isOpen,
  onClose,
  buttonRef,
}: StoryDropdownProps) {
  const [position, setPosition] = useState({ top: 0, left: 0 });
  const dropdownRef = useRef<HTMLDivElement>(null);
  const { deleteStory } = useStories();

  useEffect(() => {
    if (isOpen && buttonRef?.current) {
      const rect = buttonRef.current.getBoundingClientRect();
      setPosition({
        top: rect.bottom + window.scrollY + 4,
        left: rect.left + window.scrollX - 176 + rect.width,
      });
    }
  }, [isOpen, buttonRef]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node) &&
        buttonRef?.current &&
        !buttonRef.current.contains(event.target as Node)
      ) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen, onClose, buttonRef]);

  const handleDelete = async (e: React.MouseEvent) => {
    e.stopPropagation();
    if (
      window.confirm(
        "Are you sure you want to delete this story? This action cannot be undone."
      )
    ) {
      try {
        await deleteStory(story.id);
        onClose();
      } catch (error) {
        console.error("Error deleting story:", error);
        alert("Failed to delete story. Please try again.");
      }
    }
  };

  if (!isOpen) return null;

  return createPortal(
    <div
      ref={dropdownRef}
      className="fixed z-[9999]"
      style={{ top: position.top, left: position.left }}
    >
      <div className="w-44 bg-gray-900/90 backdrop-blur-md border border-white/5 rounded-xl shadow-xl shadow-black/20 overflow-hidden">
        <button
          className="w-full px-3.5 py-2.5 text-sm text-left hover:bg-white/5 flex items-center gap-3 text-gray-200 border-b border-white/5 transition-colors"
          onClick={(e) => {
            e.stopPropagation();
            const url = window.location.href;
            navigator.clipboard.writeText(url);
            alert("Profile URL copied to clipboard!");
            onClose();
          }}
        >
          <Share2 className="w-4 h-4 text-gray-400" />
          <span className="font-medium">Share Story</span>
        </button>

        <button
          className="w-full px-3.5 py-2.5 text-sm text-left hover:bg-white/5 flex items-center gap-3 text-gray-200 border-b border-white/5 transition-colors"
          onClick={(e) => {
            e.stopPropagation();
            const element = document.createElement("a");
            const file = new Blob([story.content], { type: "text/plain" });
            element.href = URL.createObjectURL(file);
            element.download = `${story.title}.txt`;
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
            onClose();
          }}
        >
          <Download className="w-4 h-4 text-gray-400" />
          <span className="font-medium">Download</span>
        </button>

        <button
          className="w-full px-3.5 py-2.5 text-sm text-left hover:bg-white/5 flex items-center gap-3 text-red-400 hover:text-red-300 transition-colors"
          onClick={handleDelete}
        >
          <Trash2 className="w-4 h-4" />
          <span className="font-medium">Delete Story</span>
        </button>
      </div>
    </div>,
    document.body
  );
}

export default function LibraryPage() {
  return <LibraryPageContent />;
}

function LibraryPageContent() {
  const { user } = useAuth();
  const { stories, loading, error, refreshStories, deleteStory } = useStories();
  const [selectedStory, setSelectedStory] = useState<Story | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [sortByRecent, setSortByRecent] = useState(true);
  const [openDropdownId, setOpenDropdownId] = useState<string | null>(null);
  const dropdownButtonRefs = useRef<{
    [key: string]: HTMLButtonElement | null;
  }>({});
  const { connected } = useWeb3();

  // Refresh stories when component mounts
  useEffect(() => {
    if (user) {
      void refreshStories();
    }
  }, [user, refreshStories]);

  // Filter and sort stories
  const filteredAndSortedStories = useMemo(() => {
    let result = [...stories];

    // Apply search filter
    if (searchQuery) {
      result = result.filter(
        (story) =>
          story.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          story.genre.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // Apply recent sort
    if (sortByRecent) {
      result.sort(
        (a, b) =>
          new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      );
    }

    return result;
  }, [stories, searchQuery, sortByRecent]);

  // Add useEffect for click outside handling at the component level
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const dropdowns = document.querySelectorAll(".story-dropdown");
      dropdowns.forEach((dropdown) => {
        if (!dropdown.contains(event.target as Node)) {
          dropdown.classList.add("hidden");
        }
      });
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Add delete handler
  const handleDelete = useCallback(
    async (storyId: string): Promise<void> => {
      try {
        await deleteStory(storyId);
      } catch (error) {
        console.error("Error deleting story:", error);
        throw error;
      }
    },
    [deleteStory]
  );

  if (!user && !connected) {
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
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-6xl mx-auto px-6 py-8"
      >
        <div className="flex flex-col space-y-6">
          {/* Header */}
          <div className="flex items-center justify-between">
            <h1 className="text-3xl font-bold text-gray-200">Library</h1>
          </div>

          {/* Action Bar */}
          <div className="flex items-center space-x-4">
            <div className="flex-1 max-w-md">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search by story name or genre"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 bg-gray-900/50 border border-gray-800/50 text-white placeholder-gray-500 w-full rounded-lg py-2 focus:border-green-500 focus:ring-1 focus:ring-green-500"
                />
              </div>
            </div>
            <button
              onClick={() => setSortByRecent(!sortByRecent)}
              className={`px-4 py-2 border border-gray-800/50 rounded-lg flex items-center space-x-2 transition-colors ${
                sortByRecent
                  ? "text-green-400 border-green-500/20 bg-green-500/10"
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}
            >
              <Clock className="w-4 h-4" />
              <span>Recent</span>
            </button>
          </div>

          {/* Stories List */}
          <div className="space-y-3">
            {filteredAndSortedStories.length === 0 ? (
              <div className="text-gray-400 text-center py-8">
                {searchQuery
                  ? "No stories found matching your search."
                  : "No stories found. Create your first story to get started!"}
              </div>
            ) : (
              filteredAndSortedStories.map((story) => (
                <div
                  key={story.id}
                  className="group flex items-center justify-between p-3 bg-gray-900/30 backdrop-blur-sm rounded-lg border border-gray-800/30 hover:border-green-500/20 transition-all duration-300"
                >
                  {/* Story Info */}
                  <div className="flex-1 min-w-0 flex items-center gap-4">
                    {/* Cover */}
                    <div className="w-12 h-12 bg-gradient-to-br from-green-950 via-emerald-950 to-green-950 rounded-lg flex items-center justify-center flex-shrink-0">
                      <BookOpen className="w-5 h-5 text-green-500/20" />
                    </div>

                    {/* Details */}
                    <div className="min-w-0">
                      <h3 className="text-gray-200 text-sm font-medium mb-0.5 pr-4 truncate">
                        {story.title}
                      </h3>
                      <div className="flex items-center gap-2 text-xs text-gray-500">
                        <span>{story.genre}</span>
                        <span>•</span>
                        <div className="flex items-center gap-1">
                          <BookOpen className="w-3 h-3" />
                          <span>{story.word_count} words</span>
                        </div>
                        <span>•</span>
                        <span>
                          {new Date(story.created_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => setSelectedStory(story)}
                      className="px-3 py-1.5 text-sm bg-green-500 text-black font-medium rounded-lg hover:bg-green-400 transition-all duration-200"
                    >
                      Read Story
                    </button>
                    <button
                      ref={(el) => {
                        dropdownButtonRefs.current[story.id] = el;
                      }}
                      onClick={(e) => {
                        e.stopPropagation();
                        setOpenDropdownId(
                          openDropdownId === story.id ? null : story.id
                        );
                      }}
                      className="p-1.5 hover:bg-white/5 rounded-lg transition-colors"
                    >
                      <MoreVertical className="w-4 h-4 text-gray-500" />
                    </button>
                  </div>

                  <StoryDropdown
                    story={story}
                    isOpen={openDropdownId === story.id}
                    onClose={() => setOpenDropdownId(null)}
                    buttonRef={{
                      current: dropdownButtonRefs.current[story.id],
                    }}
                  />
                </div>
              ))
            )}
          </div>
        </div>

        {selectedStory && (
          <StoryModal
            story={selectedStory}
            onClose={() => setSelectedStory(null)}
          />
        )}
      </motion.div>
    </div>
  );
}
