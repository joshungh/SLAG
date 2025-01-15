"use client";

import { useState } from "react";
import { Search as SearchIcon, Star, ThumbsUp, BookOpen } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

type ContentType = "Stories" | "Playlists" | "Users";
type SortOption = "Most relevant" | "Most recent" | "Most liked";

interface SearchResult {
  id: string;
  title: string;
  author: string;
  coverImage: string;
  genre: string;
  rating: number;
  likes: number;
  reads: number;
  description: string;
}

function SearchPage() {
  const [activeTab, setActiveTab] = useState<ContentType>("Stories");
  const [sortBy, setSortBy] = useState<SortOption>("Most relevant");
  const [searchQuery, setSearchQuery] = useState("");

  // Mock search results
  const searchResults: SearchResult[] = [
    {
      id: "1",
      title: "Lights in the Night (Remastered)",
      author: "ImOliver",
      coverImage: "https://picsum.photos/seed/story1/300/400",
      genre: "Sci-fi, Cyberpunk",
      rating: 4.5,
      likes: 2300,
      reads: 85000,
      description: "electronic dance high-energy",
    },
    {
      id: "2",
      title: "The Quantum Archaeologist",
      author: "DrQuantum",
      coverImage: "https://picsum.photos/seed/story2/300/400",
      genre: "Hard Sci-fi, Mystery",
      rating: 4.7,
      likes: 1800,
      reads: 65000,
      description: "deep space exploration mystery",
    },
    // Add more mock results...
  ];

  return (
    <div className="min-h-screen bg-black text-white p-8">
      {/* Search Header */}
      <div className="max-w-6xl mx-auto mb-8">
        <div className="relative">
          <SearchIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-6 h-6 text-gray-400" />
          <input
            type="text"
            placeholder="Search for stories, playlists, or users"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-gray-900/50 rounded-full px-12 py-4 text-lg placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-green-400/50"
          />
        </div>
      </div>

      {/* Tabs and Filters */}
      <div className="max-w-6xl mx-auto mb-8">
        <div className="flex justify-between items-center">
          <div className="flex space-x-4">
            {(["Stories", "Playlists", "Users"] as ContentType[]).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-4 py-2 rounded-lg text-base transition-colors ${
                  activeTab === tab
                    ? "bg-green-400/10 text-green-400"
                    : "text-gray-400 hover:text-white"
                }`}
              >
                {tab}
              </button>
            ))}
          </div>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as SortOption)}
            className="bg-gray-900/50 text-gray-400 px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-400/50"
          >
            <option>Most relevant</option>
            <option>Most recent</option>
            <option>Most liked</option>
          </select>
        </div>
      </div>

      {/* Search Results */}
      <motion.div
        className="max-w-6xl mx-auto space-y-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        {searchResults.map((result) => (
          <motion.div
            key={result.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex items-center gap-4 p-4 bg-gray-900/50 rounded-lg hover:bg-gray-900/70 transition-colors group"
          >
            {/* Thumbnail */}
            <div className="relative w-16 h-20 overflow-hidden rounded">
              <img
                src={result.coverImage}
                alt={result.title}
                className="object-cover w-full h-full"
              />
              <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                <BookOpen className="w-6 h-6 text-white" />
              </div>
            </div>

            {/* Content */}
            <div className="flex-grow">
              <div className="flex items-center gap-2">
                <h3 className="text-lg font-medium">{result.title}</h3>
                <span className="px-2 py-0.5 text-xs bg-green-400/20 text-green-400 rounded">
                  v4
                </span>
              </div>
              <p className="text-sm text-gray-400">{result.genre}</p>
              <p className="text-sm text-gray-500">{result.description}</p>
            </div>

            {/* Stats */}
            <div className="flex items-center gap-6">
              <div className="flex items-center gap-2 text-gray-400">
                <Star className="w-4 h-4 text-yellow-400" />
                <span>{result.rating}</span>
              </div>
              <div className="flex items-center gap-2 text-gray-400">
                <ThumbsUp className="w-4 h-4" />
                <span>{result.likes}</span>
              </div>
              <button className="px-4 py-1.5 bg-green-400 text-black rounded hover:bg-green-300 transition-colors">
                Read
              </button>
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* No Results State */}
      {searchResults.length === 0 && (
        <div className="max-w-6xl mx-auto text-center py-16">
          <p className="text-gray-400 text-lg">
            No results found. Try adjusting your search terms.
          </p>
        </div>
      )}
    </div>
  );
}

export default SearchPage;