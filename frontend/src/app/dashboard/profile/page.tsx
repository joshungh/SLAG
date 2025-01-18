"use client";

import { useEffect, useState, useCallback } from "react";
import { useWeb3 } from "@/contexts/Web3Context";
import { motion } from "framer-motion";
import {
  Edit3,
  User,
  Mail,
  Wallet,
  X,
  Camera,
  BookOpen,
  Clock,
  Share2,
  Download,
  MoreVertical,
  Globe,
  Link as LinkIcon,
  Bug,
  Flag,
  Trash2,
} from "lucide-react";
import Image from "next/image";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { DeleteStoryButton } from "@/components/DeleteStoryButton";
import { StoryProvider } from "@/contexts/StoryContext";

interface DynamoDBString {
  S: string;
}

function isDynamoDBString(value: any): value is DynamoDBString {
  return (
    value &&
    typeof value === "object" &&
    "S" in value &&
    typeof value.S === "string"
  );
}

interface UserProfile {
  username: string;
  email: string | null;
  first_name: string | null;
  last_name: string | null;
  profile_picture: string | null;
  web3_wallet: string | null;
  bio: string;
  created_at: string;
  login_methods: string[];
}

interface EditableFields {
  username: string;
  first_name: string;
  last_name: string;
}

interface Story {
  id: string;
  title: string;
  genre: string;
  word_count: number;
  created_at: string;
  content: string;
  bible: any;
  framework: any;
}

interface Activity {
  id: string;
  type: string;
  prompt: string;
  timestamp: string;
}

// Add StoryModal component
function StoryModal({ story, onClose }: { story: Story; onClose: () => void }) {
  // Add useEffect for click outside handling
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const modalContent = document.querySelector(".modal-content");
      if (modalContent && !modalContent.contains(event.target as Node)) {
        onClose();
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [onClose]);

  // Keep existing Escape key handler
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

  return (
    <div className="fixed inset-0 bg-black/90 backdrop-blur-sm z-50 overflow-y-auto">
      <div className="min-h-screen px-4 py-8">
        <div className="modal-content bg-gradient-to-br from-gray-900 to-black border border-gray-800/50 rounded-xl w-full max-w-4xl mx-auto shadow-xl">
          {/* Rest of the modal content stays the same */}
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
    </div>
  );
}

export default function ProfilePage() {
  const router = useRouter();
  const { connected, publicKey } = useWeb3();
  const { user: authUser } = useAuth();
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editableFields, setEditableFields] = useState<EditableFields>({
    username: "",
    first_name: "",
    last_name: "",
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stories, setStories] = useState<Story[]>([]);
  const [activities, setActivities] = useState<Activity[]>([]);
  const [selectedStory, setSelectedStory] = useState<Story | null>(null);

  // Redirect if not authenticated
  useEffect(() => {
    if (!authUser && !isLoading) {
      router.push("/dashboard/create");
    }
  }, [authUser, isLoading, router]);

  // Use authUser data to set profile
  useEffect(() => {
    if (authUser) {
      const processedLoginMethods = (authUser.login_methods || []).map(
        (method) => {
          if (isDynamoDBString(method)) {
            return method.S;
          }
          return typeof method === "string" ? method : String(method);
        }
      );

      const processedWallet = isDynamoDBString(authUser.web3_wallet)
        ? authUser.web3_wallet.S
        : typeof authUser.web3_wallet === "string"
        ? authUser.web3_wallet
        : null;

      setProfile({
        username: authUser.username,
        email: authUser.email,
        first_name: authUser.first_name || null,
        last_name: authUser.last_name || null,
        profile_picture: authUser.profile_picture || null,
        web3_wallet:
          typeof authUser.web3_wallet === "boolean" ? null : processedWallet,
        bio: authUser.bio || "",
        created_at: authUser.created_at,
        login_methods: processedLoginMethods,
      });
    }
  }, [authUser]);

  useEffect(() => {
    if (profile) {
      setEditableFields({
        username: profile.username,
        first_name: profile.first_name || "",
        last_name: profile.last_name || "",
      });
    }
  }, [profile]);

  const handleEditToggle = () => {
    if (isEditing) {
      // Reset fields when canceling
      setEditableFields({
        username: profile?.username || "",
        first_name: profile?.first_name || "",
        last_name: profile?.last_name || "",
      });
    }
    setIsEditing(!isEditing);
    setError(null);
  };

  const handleFieldChange = (field: keyof EditableFields, value: string) => {
    setEditableFields((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSave = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem("auth_token");
      if (!token) {
        throw new Error("No authentication token found");
      }

      const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL;
      if (!BACKEND_URL) {
        throw new Error("Backend URL not configured");
      }

      const profileData = {
        username: editableFields.username,
        first_name: editableFields.first_name,
        last_name: editableFields.last_name,
      };

      const response = await fetch(`${BACKEND_URL}/api/users/profile`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(profileData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(
          errorData.detail || errorData.error || "Failed to update profile"
        );
      }

      const updatedData = await response.json();

      // Process the updated data the same way we process initial data
      const processedLoginMethods = (updatedData.login_methods || []).map(
        (method: unknown) => {
          if (isDynamoDBString(method)) {
            return method.S;
          }
          return typeof method === "string" ? method : String(method);
        }
      );

      const processedWallet = isDynamoDBString(updatedData.web3_wallet)
        ? updatedData.web3_wallet.S
        : typeof updatedData.web3_wallet === "string"
        ? updatedData.web3_wallet
        : null;

      const processedProfile = {
        ...updatedData,
        web3_wallet:
          typeof updatedData.web3_wallet === "boolean" ? null : processedWallet,
        login_methods: processedLoginMethods,
      };

      setProfile((prev) => ({
        ...prev!,
        ...processedProfile,
      }));
      setIsEditing(false);
    } catch (err) {
      console.error("Profile update error:", err);
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  const truncateAddress = (address: string | null) => {
    if (!address || typeof address !== "string") return "";
    return `${address.slice(0, 4)}...${address.slice(-4)}`;
  };

  // Fetch stories and activities
  useEffect(() => {
    if (!authUser) return;

    let mounted = true;
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem("auth_token");
        if (!token) return;

        const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL;
        if (!BACKEND_URL) return;

        // Only fetch stories if we don't have any yet
        if (stories.length === 0) {
          // Fetch stories
          const storiesResponse = await fetch(`${BACKEND_URL}/api/stories`, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });

          if (storiesResponse.ok && mounted) {
            const data = await storiesResponse.json();
            setStories(data.stories || []);
          }
        }

        // Get recent activities from story queue
        const queueString = localStorage.getItem("storyQueue");
        if (queueString) {
          const queue = JSON.parse(queueString);
          const recentActivities = queue.map((item: any) => ({
            id: item.id,
            type: "Story Generation",
            prompt: item.prompt,
            timestamp: new Date(item.timestamp || Date.now()).toISOString(),
          }));
          if (mounted) {
            setActivities(recentActivities);
          }
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    };

    void fetchUserData();

    return () => {
      mounted = false;
    };
  }, [authUser, stories.length]); // Add stories.length to dependencies

  const handleShareProfile = async () => {
    try {
      const url = window.location.href;
      await navigator.clipboard.writeText(url);
      // You could add a toast notification here
      alert("Profile URL copied to clipboard!");
    } catch (err) {
      console.error("Failed to copy URL:", err);
    }
  };

  const handleDelete = useCallback(async (storyId: string): Promise<void> => {
    try {
      const token = localStorage.getItem("auth_token");
      if (!token) {
        throw new Error("No authentication token found");
      }

      const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL;
      if (!BACKEND_URL) {
        throw new Error("Backend URL not configured");
      }

      const response = await fetch(`${BACKEND_URL}/api/stories/${storyId}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to delete story");
      }

      // Update local state
      setStories((prev) => prev.filter((story) => story.id !== storyId));
    } catch (error) {
      console.error("Error deleting story:", error);
      throw error; // Re-throw to let DeleteStoryButton handle the error
    }
  }, []);

  // Add useEffect for click outside handling
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

  if (!profile) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-green-500 mb-4"></div>
        <div className="text-gray-400 text-sm">
          {!authUser ? (
            "Waiting for authentication..."
          ) : error ? (
            <span className="text-red-500">{error}</span>
          ) : (
            "Loading profile..."
          )}
        </div>
      </div>
    );
  }

  return (
    <StoryProvider>
      <div className="min-h-screen bg-black">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-6xl mx-auto px-6 py-8"
        >
          {/* Profile Header - Suno-like layout */}
          <div className="bg-gradient-to-br from-gray-900 to-black rounded-2xl p-8 mb-12 border border-gray-800/50">
            <div className="flex flex-col md:flex-row md:items-center gap-8">
              {/* Profile Picture */}
              <div className="relative flex-shrink-0">
                <div className="w-[140px] h-[140px] rounded-full overflow-hidden">
                  {profile?.profile_picture ? (
                    <Image
                      src={profile.profile_picture}
                      alt="Profile"
                      width={140}
                      height={140}
                      className="object-cover"
                    />
                  ) : (
                    <div className="w-full h-full bg-gradient-to-br from-green-400/20 to-green-600/20 flex items-center justify-center">
                      <User className="w-12 h-12 text-green-400" />
                    </div>
                  )}
                </div>
              </div>

              {/* Profile Info */}
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between mb-6">
                  <div className="min-w-0 flex-1">
                    {isEditing ? (
                      <div className="space-y-4 max-w-lg">
                        <input
                          type="text"
                          value={editableFields.username}
                          onChange={(e) =>
                            handleFieldChange("username", e.target.value)
                          }
                          className="block w-full px-4 py-2.5 bg-black/50 border border-gray-700 rounded-lg focus:border-green-500 focus:ring-1 focus:ring-green-500 text-white text-lg"
                          placeholder="Username"
                        />
                        <div className="flex gap-4">
                          <input
                            type="text"
                            value={editableFields.first_name}
                            onChange={(e) =>
                              handleFieldChange("first_name", e.target.value)
                            }
                            className="block w-full px-4 py-2.5 bg-black/50 border border-gray-700 rounded-lg focus:border-green-500 focus:ring-1 focus:ring-green-500 text-white"
                            placeholder="First Name"
                          />
                          <input
                            type="text"
                            value={editableFields.last_name}
                            onChange={(e) =>
                              handleFieldChange("last_name", e.target.value)
                            }
                            className="block w-full px-4 py-2.5 bg-black/50 border border-gray-700 rounded-lg focus:border-green-500 focus:ring-1 focus:ring-green-500 text-white"
                            placeholder="Last Name"
                          />
                        </div>
                      </div>
                    ) : (
                      <>
                        <h1 className="text-3xl md:text-4xl font-bold mb-2 truncate">
                          {profile?.username}
                        </h1>
                        {(profile?.first_name || profile?.last_name) && (
                          <p className="text-gray-400 text-lg truncate">
                            {[profile.first_name, profile.last_name]
                              .filter(Boolean)
                              .join(" ")}
                          </p>
                        )}
                      </>
                    )}
                    {profile?.email && (
                      <div className="flex items-center space-x-2 text-gray-400 mt-3">
                        <Mail className="w-4 h-4" />
                        <span className="truncate">{profile.email}</span>
                      </div>
                    )}
                  </div>
                  <div className="flex space-x-2 ml-4 flex-shrink-0">
                    {isEditing ? (
                      <>
                        <button
                          onClick={handleSave}
                          disabled={isLoading}
                          className="px-4 py-2 bg-green-500 text-black font-medium rounded-lg hover:bg-green-400 transition-colors disabled:opacity-50"
                        >
                          {isLoading ? "Saving..." : "Save"}
                        </button>
                        <button
                          onClick={handleEditToggle}
                          className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                        >
                          <X className="w-5 h-5" />
                        </button>
                      </>
                    ) : (
                      <button
                        onClick={handleEditToggle}
                        className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                      >
                        <Edit3 className="w-5 h-5" />
                      </button>
                    )}
                  </div>
                </div>

                {error && (
                  <div className="mt-4 p-3 bg-red-500/10 border border-red-500 rounded-lg text-red-500 text-sm">
                    {error}
                  </div>
                )}

                {/* Stats */}
                <div className="flex items-center space-x-8 text-gray-400">
                  <div className="flex items-center space-x-2">
                    <BookOpen className="w-4 h-4" />
                    <span>{stories.length} Stories</span>
                  </div>
                  <button
                    onClick={handleShareProfile}
                    className="flex items-center space-x-2 hover:text-white transition-colors"
                  >
                    <Share2 className="w-4 h-4" />
                    <span>Share Profile</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Navigation Tabs */}
          <div className="border-b border-gray-800 mb-8 px-2">
            <div className="flex space-x-8">
              <div className="px-4 py-2 text-green-400 border-b-2 border-green-400">
                Stories
              </div>
            </div>
          </div>

          {/* Stories Grid */}
          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
            {stories.map((story) => (
              <div
                key={story.id}
                className="group bg-gray-900/50 backdrop-blur-sm rounded-xl overflow-visible border border-gray-800/50 hover:border-green-500/20 transition-all duration-300 hover:shadow-lg hover:shadow-green-500/10"
              >
                {/* Clickable Story Area */}
                <div
                  className="relative cursor-pointer"
                  onClick={() => setSelectedStory(story)}
                >
                  {/* Cover Image Area */}
                  <div className="aspect-[3/2] bg-gradient-to-br from-green-500/5 via-emerald-500/5 to-green-500/5 relative">
                    <div className="absolute inset-0 flex items-center justify-center">
                      <BookOpen className="w-8 h-8 text-green-500/20" />
                    </div>

                    {/* Hover Overlay */}
                    <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-all duration-300 flex items-center justify-center backdrop-blur-sm">
                      <button className="px-5 py-2 bg-green-500 text-black font-medium rounded-lg hover:bg-green-400 transition-all duration-200 transform group-hover:scale-105">
                        Read Story
                      </button>
                    </div>
                  </div>
                </div>

                {/* Bottom Info Container */}
                <div className="p-4 space-y-2">
                  {/* Title and Menu Row */}
                  <div className="flex items-start justify-between gap-2">
                    <h3 className="font-medium text-white text-sm leading-5">
                      {story.title}
                    </h3>

                    {/* More Options Button */}
                    <div className="relative flex-shrink-0">
                      <button
                        onClick={(e) => {
                          e.preventDefault();
                          e.stopPropagation();
                          // Close all other dropdowns first
                          const allDropdowns =
                            document.querySelectorAll(".story-dropdown");
                          allDropdowns.forEach((el) => {
                            if (el !== e.currentTarget.nextElementSibling) {
                              el.classList.add("hidden");
                            }
                          });
                          // Toggle this dropdown
                          const dropdown = e.currentTarget.nextElementSibling;
                          dropdown?.classList.toggle("hidden");
                        }}
                        className="p-1 -mr-1 hover:bg-white/10 rounded-lg transition-colors"
                      >
                        <MoreVertical className="w-4 h-4 text-gray-400" />
                      </button>

                      {/* Main Dropdown Menu */}
                      <div className="story-dropdown hidden absolute right-0 top-full mt-1.5 w-48 bg-gray-900/90 backdrop-blur-md border border-white/5 rounded-xl shadow-xl shadow-black/20 z-50">
                        {/* Share Option */}
                        <button
                          className="w-full px-4 py-3 text-sm text-left hover:bg-white/5 flex items-center gap-3 text-gray-200 border-b border-white/5 transition-colors"
                          onClick={(e) => {
                            e.stopPropagation();
                            const url = window.location.href;
                            navigator.clipboard.writeText(url);
                            alert("Profile URL copied to clipboard!");
                            e.currentTarget
                              .closest(".story-dropdown")
                              ?.classList.add("hidden");
                          }}
                        >
                          <Share2 className="w-4 h-4 text-gray-400" />
                          <span className="font-medium">Share Story</span>
                        </button>

                        {/* Download Option */}
                        <button
                          className="w-full px-4 py-3 text-sm text-left hover:bg-white/5 flex items-center gap-3 text-gray-200 transition-colors"
                          onClick={(e) => {
                            e.stopPropagation();
                            const element = document.createElement("a");
                            const file = new Blob([story.content], {
                              type: "text/plain",
                            });
                            element.href = URL.createObjectURL(file);
                            element.download = `${story.title}.txt`;
                            document.body.appendChild(element);
                            element.click();
                            document.body.removeChild(element);
                            e.currentTarget
                              .closest(".story-dropdown")
                              ?.classList.add("hidden");
                          }}
                        >
                          <Download className="w-4 h-4 text-gray-400" />
                          <span className="font-medium">Download</span>
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Genre */}
                  <div className="text-xs text-gray-400">{story.genre}</div>

                  {/* Word Count */}
                  <div className="flex items-center gap-1.5 text-xs text-gray-500">
                    <BookOpen className="w-3.5 h-3.5" />
                    <span>{story.word_count} words</span>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {selectedStory && (
            <StoryModal
              story={selectedStory}
              onClose={() => setSelectedStory(null)}
            />
          )}
        </motion.div>
      </div>
    </StoryProvider>
  );
}
