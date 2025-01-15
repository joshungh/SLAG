"use client";

import { useState, useEffect } from "react";
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
  const downloadStory = () => {
    const content = `# ${story.title}\n\n${story.content}`;
    const blob = new Blob([content], { type: "text/plain" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${story.title.toLowerCase().replace(/\s+/g, "-")}.txt`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  };

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center p-4 z-50">
      <div className="bg-gray-900 rounded-lg w-full max-w-4xl max-h-[90vh] overflow-y-auto">
        <div className="p-6 space-y-6">
          {/* Header */}
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold text-white">{story.title}</h2>
            <div className="space-x-2">
              <button
                onClick={downloadStory}
                className="px-4 py-2 bg-green-400 text-black rounded hover:bg-green-300"
              >
                Download
              </button>
              <button
                onClick={onClose}
                className="px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-600"
              >
                Close
              </button>
            </div>
          </div>

          {/* Story Content */}
          <div className="space-y-4">
            <h3 className="text-xl text-green-400">Story</h3>
            <div className="bg-gray-800/50 p-4 rounded whitespace-pre-wrap text-gray-300">
              {story.content || ""}
            </div>
          </div>

          {/* Story Bible */}
          <div className="space-y-4">
            <h3 className="text-xl text-green-400">Story Bible</h3>
            <div className="bg-gray-800/50 p-4 rounded">
              <pre className="text-gray-300 overflow-x-auto">
                {JSON.stringify(story.bible, null, 2)}
              </pre>
            </div>
          </div>

          {/* Story Framework */}
          <div className="space-y-4">
            <h3 className="text-xl text-green-400">Story Framework</h3>
            <div className="bg-gray-800/50 p-4 rounded">
              <pre className="text-gray-300 overflow-x-auto">
                {JSON.stringify(story.framework, null, 2)}
              </pre>
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

  useEffect(() => {
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
  }, []);

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
