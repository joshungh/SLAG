"use client";

import { useState } from "react";
import {
  Search,
  BookOpen,
  ListFilter,
  Heart,
  Users,
  History,
} from "lucide-react";

interface Story {
  id: string;
  title: string;
  author: string;
  genre: string;
  wordCount: number;
  version: string;
  isPublic: boolean;
  coverImage: string;
  rating: number;
  likes: number;
  reads: number;
}

export default function LibraryPage() {
  const [activeTab, setActiveTab] = useState<
    "stories" | "collections" | "following" | "followers" | "history"
  >("stories");
  const [filterType, setFilterType] = useState<"scenes" | "liked" | "public">(
    "scenes"
  );

  // Mock data
  const stories: Story[] = [
    {
      id: "1",
      title: "Lights in the Night (Remastered)",
      author: "ImOliver",
      genre: "Sci-fi, Cyberpunk",
      wordCount: 15000,
      version: "v4",
      isPublic: true,
      coverImage: "https://picsum.photos/seed/story1/300/400",
      rating: 4.5,
      likes: 2300,
      reads: 85000,
    },
    {
      id: "2",
      title: "The Quantum Archaeologist",
      author: "DrQuantum",
      genre: "Hard Sci-fi, Mystery",
      wordCount: 12000,
      version: "v4",
      isPublic: true,
      coverImage: "https://picsum.photos/seed/story2/300/400",
      rating: 4.7,
      likes: 1800,
      reads: 65000,
    },
    {
      id: "3",
      title: "Chronicles of the Starborn",
      author: "CosmicWriter",
      genre: "Space Opera, Adventure",
      wordCount: 18000,
      version: "v4",
      isPublic: false,
      coverImage: "https://picsum.photos/seed/story3/300/400",
      rating: 4.3,
      likes: 3100,
      reads: 92000,
    },
    {
      id: "4",
      title: "Whispers in the Machine",
      author: "TechnoTeller",
      genre: "Cyberpunk, Horror",
      wordCount: 9000,
      version: "v4",
      isPublic: true,
      coverImage: "https://picsum.photos/seed/story4/300/400",
      rating: 4.8,
      likes: 4200,
      reads: 120000,
    },
    {
      id: "5",
      title: "Echoes of Tomorrow",
      author: "ElenaScribe",
      genre: "Post-apocalyptic, Romance",
      wordCount: 14500,
      version: "v4",
      isPublic: true,
      coverImage: "https://picsum.photos/seed/story5/300/400",
      rating: 4.6,
      likes: 2800,
      reads: 78000,
    },
  ];

  return (
    <div className="min-h-screen bg-black">
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="flex flex-col space-y-6">
          {/* Navigation Tabs */}
          <div className="flex border-b border-gray-800">
            <button
              onClick={() => setActiveTab("stories")}
              className={`px-6 py-4 text-base font-medium ${
                activeTab === "stories"
                  ? "text-green-400 border-b-2 border-green-400"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              Stories
            </button>
            <button
              onClick={() => setActiveTab("collections")}
              className={`px-6 py-4 text-base font-medium ${
                activeTab === "collections"
                  ? "text-green-400 border-b-2 border-green-400"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              Collections
            </button>
            <button
              onClick={() => setActiveTab("following")}
              className={`px-6 py-4 text-base font-medium ${
                activeTab === "following"
                  ? "text-green-400 border-b-2 border-green-400"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              Following
            </button>
            <button
              onClick={() => setActiveTab("followers")}
              className={`px-6 py-4 text-base font-medium ${
                activeTab === "followers"
                  ? "text-green-400 border-b-2 border-green-400"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              Followers
            </button>
            <button
              onClick={() => setActiveTab("history")}
              className={`px-6 py-4 text-base font-medium ${
                activeTab === "history"
                  ? "text-green-400 border-b-2 border-green-400"
                  : "text-gray-400 hover:text-white"
              }`}
            >
              History
            </button>
          </div>

          {/* Search and Filter Bar */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => setFilterType("scenes")}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-base ${
                  filterType === "scenes"
                    ? "bg-green-400/10 text-green-400"
                    : "text-gray-400 hover:text-white"
                }`}
              >
                <BookOpen className="w-5 h-5" />
                <span>Scenes</span>
              </button>
              <button
                onClick={() => setFilterType("liked")}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-base ${
                  filterType === "liked"
                    ? "bg-green-400/10 text-green-400"
                    : "text-gray-400 hover:text-white"
                }`}
              >
                <Heart className="w-5 h-5" />
                <span>Liked</span>
              </button>
              <button
                onClick={() => setFilterType("public")}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-base ${
                  filterType === "public"
                    ? "bg-green-400/10 text-green-400"
                    : "text-gray-400 hover:text-white"
                }`}
              >
                <Users className="w-5 h-5" />
                <span>Public</span>
              </button>
            </div>
            <div className="relative">
              <input
                type="text"
                placeholder="Search by story name, genre or synopsis"
                className="w-96 bg-gray-900/50 rounded-lg px-4 py-2 pl-10 text-base text-white placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-green-400/50"
              />
              <Search className="w-5 h-5 text-gray-500 absolute left-3 top-1/2 -translate-y-1/2" />
            </div>
          </div>

          {/* Stories List */}
          <div className="space-y-2">
            {stories.map((story) => (
              <div
                key={story.id}
                className="flex items-center justify-between p-4 bg-gray-900/50 rounded-lg hover:bg-gray-900/70"
              >
                <div className="flex items-center space-x-4">
                  <img
                    src={story.coverImage}
                    alt={story.title}
                    className="w-12 h-16 object-cover rounded"
                  />
                  <div>
                    <div className="flex items-center space-x-2">
                      <h3 className="text-white text-lg font-medium">
                        {story.title}
                      </h3>
                      <span className="px-2 py-0.5 text-sm bg-green-400/20 text-green-400 rounded">
                        {story.version}
                      </span>
                    </div>
                    <p className="text-base text-gray-400">{story.genre}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-8">
                  <button className="px-4 py-1.5 bg-green-400 text-black rounded hover:bg-green-300 transition-colors text-base">
                    Extend
                  </button>
                  <div className="flex items-center space-x-2">
                    <Heart className="w-5 h-5" />
                    <span className="text-base">{story.likes}</span>
                  </div>
                  <button className="text-gray-400 hover:text-white">
                    <ListFilter className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
