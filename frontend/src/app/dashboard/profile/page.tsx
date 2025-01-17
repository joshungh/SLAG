"use client";

import { useEffect, useState } from "react";
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
} from "lucide-react";
import Image from "next/image";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import Link from "next/link";

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

    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem("auth_token");
        if (!token) return;

        const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL;
        if (!BACKEND_URL) return;

        // Fetch stories
        const storiesResponse = await fetch(`${BACKEND_URL}/api/stories`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (storiesResponse.ok) {
          const data = await storiesResponse.json();
          setStories(data.stories || []);
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
          setActivities(recentActivities);
        }
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    };

    fetchUserData();
  }, [authUser]);

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
    <div className="container mx-auto px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-6xl mx-auto"
      >
        {/* Profile Header - Suno-like layout */}
        <div className="flex items-center space-x-8 mb-12">
          {/* Profile Picture */}
          <div className="relative">
            <div className="w-[180px] h-[180px] rounded-full overflow-hidden">
              {profile?.profile_picture ? (
                <Image
                  src={profile.profile_picture}
                  alt="Profile"
                  width={180}
                  height={180}
                  className="object-cover"
                />
              ) : (
                <div className="w-full h-full bg-gradient-to-br from-green-400/20 to-green-600/20 flex items-center justify-center">
                  <User className="w-16 h-16 text-green-400" />
                </div>
              )}
            </div>
          </div>

          {/* Profile Info */}
          <div className="flex-1">
            <div className="flex items-start justify-between mb-4">
              <div>
                {isEditing ? (
                  <div className="space-y-4">
                    <input
                      type="text"
                      value={editableFields.username}
                      onChange={(e) =>
                        handleFieldChange("username", e.target.value)
                      }
                      className="block w-full px-3 py-2 bg-black/50 border border-gray-700 rounded-lg focus:border-green-500 focus:ring-1 focus:ring-green-500 text-white text-lg"
                      placeholder="Username"
                    />
                    <div className="flex gap-3">
                      <input
                        type="text"
                        value={editableFields.first_name}
                        onChange={(e) =>
                          handleFieldChange("first_name", e.target.value)
                        }
                        className="block w-full px-3 py-2 bg-black/50 border border-gray-700 rounded-lg focus:border-green-500 focus:ring-1 focus:ring-green-500 text-white"
                        placeholder="First Name"
                      />
                      <input
                        type="text"
                        value={editableFields.last_name}
                        onChange={(e) =>
                          handleFieldChange("last_name", e.target.value)
                        }
                        className="block w-full px-3 py-2 bg-black/50 border border-gray-700 rounded-lg focus:border-green-500 focus:ring-1 focus:ring-green-500 text-white"
                        placeholder="Last Name"
                      />
                    </div>
                  </div>
                ) : (
                  <>
                    <h1 className="text-4xl font-bold mb-2">
                      {profile?.username}
                    </h1>
                    {(profile?.first_name || profile?.last_name) && (
                      <p className="text-gray-400 text-lg">
                        {[profile.first_name, profile.last_name]
                          .filter(Boolean)
                          .join(" ")}
                      </p>
                    )}
                  </>
                )}
                {profile?.email && (
                  <div className="flex items-center space-x-2 text-gray-400 mt-2">
                    <Mail className="w-4 h-4" />
                    <span>{profile.email}</span>
                  </div>
                )}
              </div>
              <div className="flex space-x-2">
                {isEditing ? (
                  <>
                    <button
                      onClick={handleSave}
                      disabled={isLoading}
                      className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors disabled:opacity-50"
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

        {/* Navigation Tabs */}
        <div className="border-b border-gray-800 mb-8">
          <div className="flex space-x-8">
            <div className="px-4 py-2 text-green-400 border-b-2 border-green-400">
              Stories
            </div>
          </div>
        </div>

        {/* Stories Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 mb-8">
          {stories.map((story) => (
            <div
              key={story.id}
              onClick={() => setSelectedStory(story)}
              className="cursor-pointer"
            >
              <div className="bg-black/30 backdrop-blur-lg rounded-lg overflow-hidden hover:bg-black/40 transition-colors">
                <div className="aspect-[4/3] bg-gradient-to-br from-green-400/10 to-green-600/10 flex items-center justify-center">
                  <BookOpen className="w-8 h-8 text-green-400/50" />
                </div>
                <div className="p-3">
                  <h3 className="font-medium text-white mb-1 line-clamp-1 text-sm">
                    {story.title}
                  </h3>
                  <div className="flex items-center justify-between text-xs text-gray-400">
                    <span>{story.genre}</span>
                    <span>{story.word_count} words</span>
                  </div>
                  <div className="mt-1 text-xs text-gray-500">
                    {new Date(story.created_at).toLocaleDateString()}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Story Modal */}
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
