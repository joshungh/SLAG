"use client";

import StoryCard from "@/components/StoryCard";
import { useState } from "react";
import {
  ChevronLeft,
  ChevronRight,
  Star,
  Globe,
  Clock,
  Sparkles,
  BookOpen,
  Heart,
  UserCheck,
} from "lucide-react";

interface Story {
  id: string;
  title: string;
  wordCount: number;
  likes: number;
  reads: number;
  coverImage: string;
  author: string;
  genres: string[];
  synopsis: string;
  rating: number;
  comments: number;
  dateCreated: string;
  isFollowing?: boolean;
  isLiked?: boolean;
}

export default function DashboardPage() {
  const [selectedStory, setSelectedStory] = useState<Story | null>(null);

  // Mock data for different sections
  const mockStories = (prefix: string, count: number = 8): Story[] =>
    Array.from({ length: count }, (_, i) => ({
      id: `${prefix}-${i + 1}`,
      title: [
        "The Last Guardian of the Void",
        "Echoes of Tomorrow",
        "Chronicles of the Starborn",
        "Whispers in the Machine",
        "The Quantum Archaeologist",
        "Neon Dreams",
        "The Memory Merchants",
        "Stellar Shadows",
      ][i % 8],
      wordCount: Math.floor(Math.random() * 20000) + 5000,
      likes: Math.floor(Math.random() * 5000),
      reads: Math.floor(Math.random() * 100000),
      coverImage: `https://picsum.photos/seed/${prefix}-${i + 1}/300/400`,
      author: [
        "ImOliver",
        "ElenaScribe",
        "CosmicWriter",
        "TechnoTeller",
        "DrQuantum",
        "NightWriter",
        "MindScribe",
        "StarWeaver",
      ][i % 8],
      genres: ["Sci-Fi", "Fantasy", "Cyberpunk"].slice(
        0,
        Math.floor(Math.random() * 3) + 1
      ),
      synopsis: "A captivating story of adventure and discovery...",
      rating: (Math.random() * 2 + 3).toFixed(1),
      comments: Math.floor(Math.random() * 200),
      dateCreated: new Date(
        Date.now() - Math.random() * 10000000000
      ).toISOString(),
      isFollowing: Math.random() > 0.5,
      isLiked: Math.random() > 0.5,
    }));

  const globalTrending = mockStories("trending");
  const freshStories = mockStories("fresh");
  const newStories = mockStories("new");
  const followingStories = mockStories("following");
  const likedStories = mockStories("liked");

  const scrollContainer = (
    direction: "left" | "right",
    containerId: string
  ) => {
    const container = document.getElementById(containerId);
    if (container) {
      const scrollAmount = 800;
      container.scrollBy({
        left: direction === "left" ? -scrollAmount : scrollAmount,
        behavior: "smooth",
      });
    }
  };

  const StorySection = ({
    id,
    title,
    icon: Icon,
    stories,
    actions,
  }: {
    id: string;
    title: string;
    icon: any;
    stories: Story[];
    actions?: React.ReactNode;
  }) => (
    <section className="relative mb-12">
      <div className="flex justify-between items-center mb-6">
        <div className="flex items-center space-x-3">
          <Icon className="w-6 h-6 text-green-400" />
          <h2 className="text-2xl font-serif">{title}</h2>
        </div>
        {actions}
      </div>

      <div className="relative">
        {/* Left Arrow - Keep group hover only for arrows */}
        <div className="group">
          <button
            onClick={() => scrollContainer("left", id)}
            className="absolute left-0 top-1/2 -translate-y-1/2 z-10 p-2 rounded-full bg-black/60 hover:bg-black/80 transition-all opacity-0 group-hover:opacity-100 -translate-x-1/2"
            aria-label="Scroll left"
          >
            <ChevronLeft className="w-6 h-6 text-white" />
          </button>

          {/* Right Arrow */}
          <button
            onClick={() => scrollContainer("right", id)}
            className="absolute right-0 top-1/2 -translate-y-1/2 z-10 p-2 rounded-full bg-black/60 hover:bg-black/80 transition-all opacity-0 group-hover:opacity-100 translate-x-1/2"
            aria-label="Scroll right"
          >
            <ChevronRight className="w-6 h-6 text-white" />
          </button>

          <div
            id={id}
            className="flex gap-4 overflow-x-auto scrollbar-hide scroll-smooth"
            style={{
              scrollSnapType: "x mandatory",
              WebkitOverflowScrolling: "touch",
              msOverflowStyle: "none",
              scrollbarWidth: "none",
            }}
          >
            {stories.map((story) => (
              <div
                key={story.id}
                className="flex-none w-[calc((100%-32px)/2)] sm:w-[calc((100%-48px)/3)] md:w-[calc((100%-64px)/4)] lg:w-[calc((100%-64px)/5)]"
                style={{ scrollSnapAlign: "start" }}
              >
                <StoryCard
                  {...story}
                  onPreview={() => setSelectedStory(story)}
                />
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );

  return (
    <div className="p-6">
      <StorySection
        id="global-trending"
        title="Global Trending"
        icon={Globe}
        stories={globalTrending}
        actions={
          <div className="flex space-x-3">
            <button className="text-gray-400 hover:text-white">Global</button>
            <button className="text-gray-400 hover:text-white">Now</button>
          </div>
        }
      />

      <StorySection
        id="fresh-stories"
        title="Fresh Stories"
        icon={Sparkles}
        stories={freshStories}
      />

      <StorySection
        id="new-stories"
        title="New Stories"
        icon={Clock}
        stories={newStories}
      />

      <StorySection
        id="following"
        title="Following"
        icon={UserCheck}
        stories={followingStories}
      />

      <StorySection
        id="liked"
        title="Liked Stories"
        icon={Heart}
        stories={likedStories}
      />

      {/* Preview Modal */}
      {selectedStory && (
        <div className="fixed inset-0 bg-black/80 flex items-center justify-center p-6 z-50">
          <div className="bg-gray-900 rounded-lg max-w-4xl w-full max-h-[80vh] overflow-auto">
            <div className="flex justify-between items-start p-6 border-b border-gray-800">
              <div>
                <h2 className="text-2xl font-bold mb-2">
                  {selectedStory.title}
                </h2>
                <div className="flex items-center space-x-4">
                  <p className="text-gray-400">by {selectedStory.author}</p>
                  <div className="flex items-center">
                    <Star className="w-4 h-4 text-yellow-400 fill-current" />
                    <span className="ml-1 text-gray-400">
                      {selectedStory.rating}
                    </span>
                  </div>
                </div>
              </div>
              <button
                onClick={() => setSelectedStory(null)}
                className="text-gray-400 hover:text-white"
              >
                Close
              </button>
            </div>
            <div className="p-6">
              <p className="text-gray-300 mb-4">{selectedStory.synopsis}</p>
              <div className="prose prose-invert max-w-none">
                {/* Add preview content here */}
                <p>Preview content would go here...</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
