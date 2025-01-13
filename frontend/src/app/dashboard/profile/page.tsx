"use client";

import { useEffect, useState } from "react";
import { useWeb3 } from "@/contexts/Web3Context";
import { motion } from "framer-motion";
import { Edit3, User, Mail, Wallet, X, Camera } from "lucide-react";
import Image from "next/image";
import { useAuth } from "@/contexts/AuthContext";

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

export default function ProfilePage() {
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
  const [profilePicture, setProfilePicture] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  // Use authUser data to set profile
  useEffect(() => {
    if (authUser) {
      setProfile({
        username: authUser.username,
        email: authUser.email,
        first_name: authUser.first_name || null,
        last_name: authUser.last_name || null,
        profile_picture: authUser.profile_picture || null,
        web3_wallet: authUser.web3_wallet || null,
        bio: authUser.bio || "",
        created_at: authUser.created_at,
        login_methods: authUser.login_methods || [],
      });
    } else {
      setError("Please sign in to view your profile");
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
      setPreviewUrl(null);
      setProfilePicture(null);
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

  const handleProfilePictureChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = e.target.files?.[0];
    if (file) {
      if (file.size > 5 * 1024 * 1024) {
        // 5MB limit
        setError("Profile picture must be less than 5MB");
        return;
      }
      setProfilePicture(file);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  const handleSave = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem("auth_token");
      if (!token) {
        throw new Error("No authentication token found");
      }

      const formData = new FormData();
      formData.append("username", editableFields.username);
      formData.append("first_name", editableFields.first_name);
      formData.append("last_name", editableFields.last_name);
      if (profilePicture) {
        formData.append("profile_picture", profilePicture);
      }

      const response = await fetch("/api/users/profile", {
        method: "PUT",
        body: formData,
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Failed to update profile");
      }

      const updatedProfile = await response.json();
      setProfile((prev) => ({
        ...prev!,
        ...updatedProfile,
      }));
      setIsEditing(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsLoading(false);
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
        className="max-w-4xl mx-auto"
      >
        {/* Profile Header */}
        <div className="bg-black/30 backdrop-blur-lg rounded-lg p-8 mb-8">
          <div className="flex items-start justify-between">
            <div className="flex items-center space-x-6">
              <div className="relative group">
                {isEditing ? (
                  <label className="cursor-pointer block relative">
                    <div className="w-[120px] h-[120px] rounded-full overflow-hidden">
                      {previewUrl || profile.profile_picture ? (
                        <Image
                          src={previewUrl || profile.profile_picture!}
                          alt="Profile preview"
                          width={120}
                          height={120}
                          className="object-cover"
                        />
                      ) : (
                        <div className="w-full h-full bg-gradient-to-br from-green-400/20 to-green-600/20 flex items-center justify-center">
                          <User className="w-12 h-12 text-green-400" />
                        </div>
                      )}
                      <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                        <Camera className="w-6 h-6 text-white" />
                      </div>
                    </div>
                    <input
                      type="file"
                      accept="image/*"
                      className="hidden"
                      onChange={handleProfilePictureChange}
                    />
                  </label>
                ) : (
                  <div className="w-[120px] h-[120px] rounded-full overflow-hidden">
                    {profile.profile_picture ? (
                      <Image
                        src={profile.profile_picture}
                        alt={profile.username}
                        width={120}
                        height={120}
                        className="object-cover"
                      />
                    ) : (
                      <div className="w-full h-full bg-gradient-to-br from-green-400/20 to-green-600/20 flex items-center justify-center">
                        <User className="w-12 h-12 text-green-400" />
                      </div>
                    )}
                  </div>
                )}
              </div>
              <div className="space-y-2">
                {isEditing ? (
                  <div className="space-y-3">
                    <input
                      type="text"
                      value={editableFields.username}
                      onChange={(e) =>
                        handleFieldChange("username", e.target.value)
                      }
                      className="block w-full px-3 py-2 bg-black/50 border border-gray-700 rounded-lg focus:border-green-500 focus:ring-1 focus:ring-green-500 text-white"
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
                    <h1 className="text-3xl font-bold mb-2">
                      {profile.username}
                    </h1>
                    {(profile.first_name || profile.last_name) && (
                      <p className="text-gray-400">
                        {[profile.first_name, profile.last_name]
                          .filter(Boolean)
                          .join(" ")}
                      </p>
                    )}
                  </>
                )}
                <div className="text-gray-400 space-y-1">
                  {profile.email && (
                    <div className="flex items-center space-x-2">
                      <Mail className="w-4 h-4" />
                      <span>{profile.email}</span>
                    </div>
                  )}
                  {profile.web3_wallet && (
                    <div className="flex items-center space-x-2">
                      <Wallet className="w-4 h-4" />
                      <span>{`${profile.web3_wallet.slice(
                        0,
                        4
                      )}...${profile.web3_wallet.slice(-4)}`}</span>
                    </div>
                  )}
                </div>
              </div>
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
        </div>

        {/* Rest of the profile content */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="space-y-6">
            <div className="bg-black/30 backdrop-blur-lg rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">About</h2>
              <p className="text-gray-300">{profile.bio}</p>
            </div>
            <div className="bg-black/30 backdrop-blur-lg rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Login Methods</h2>
              <div className="space-y-2">
                {profile.login_methods.map((method) => (
                  <div
                    key={method}
                    className="flex items-center space-x-2 text-gray-300"
                  >
                    {method === "EMAIL" ? (
                      <Mail className="w-4 h-4" />
                    ) : (
                      <Wallet className="w-4 h-4" />
                    )}
                    <span>{method}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column - Stories & Activity */}
          <div className="md:col-span-2 space-y-6">
            <div className="bg-black/30 backdrop-blur-lg rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Your Stories</h2>
              {/* TODO: Add stories grid */}
              <p className="text-gray-400">No stories yet</p>
            </div>
            <div className="bg-black/30 backdrop-blur-lg rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
              {/* TODO: Add activity feed */}
              <p className="text-gray-400">No recent activity</p>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
