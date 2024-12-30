"use client";

import { BookOpen, Star, ThumbsUp } from "lucide-react";

interface StoryCardProps {
  title: string;
  wordCount: number;
  likes: number;
  reads: number;
  coverImage: string;
  author: string;
  genres: string[];
  synopsis: string;
  onPreview: () => void;
  rating: number;
  comments: number;
  isFollowing?: boolean;
  isLiked?: boolean;
}

export default function StoryCard({
  title,
  wordCount,
  likes,
  reads,
  coverImage,
  author,
  genres,
  synopsis,
  onPreview,
  rating,
  comments,
  isFollowing,
  isLiked,
}: StoryCardProps) {
  // Function to format numbers (e.g., 1500 -> 1.5k)
  const formatNumber = (num: number) => {
    if (num >= 1000000) {
      return `${(num / 1000000).toFixed(1)}M`;
    }
    if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}k`;
    }
    return num.toString();
  };

  return (
    <div className="group relative bg-gray-900/50 rounded-lg overflow-hidden">
      {/* Book Cover */}
      <div className="aspect-[3/4] relative overflow-hidden">
        <img
          src={coverImage}
          alt={title}
          className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-300"
        />
        {/* Likes Badge */}
        <div className="absolute top-2 right-2 bg-black/60 px-2 py-1 rounded text-sm flex items-center space-x-1">
          <ThumbsUp
            className={`w-3 h-3 ${
              isLiked ? "fill-green-500 text-green-500" : "text-gray-300"
            }`}
          />
          <span>{formatNumber(likes)}</span>
        </div>
        <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
          <button
            onClick={onPreview}
            className="bg-green-400 text-black rounded-lg px-3 py-1.5 flex items-center space-x-1 hover:bg-green-300 transition-colors text-sm"
          >
            <BookOpen className="w-4 h-4" />
            <span>Preview</span>
          </button>
        </div>
      </div>

      {/* Story Info */}
      <div className="p-3">
        <h3 className="text-base font-medium mb-1 truncate">{title}</h3>
        <div className="flex items-center justify-between text-xs text-gray-400">
          <span className="font-medium truncate">{author}</span>
          <div className="flex items-center space-x-2">
            <Star className="w-3 h-3 text-yellow-400 fill-current" />
            <span>{rating}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
