"use client";

import { useState } from "react";
import { Shuffle, Wand2, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface Genre {
  id: string;
  label: string;
  color: string;
  description: string;
  themes: string[];
  bgImage?: string;
}

function ExplorePage() {
  const [selectedGenre, setSelectedGenre] = useState<string | null>(null);

  const genres: Genre[] = [
    {
      id: "mechanical-era",
      label: "Mechanical Era",
      color: "#D4B483", // Warm sand color
      description:
        "Chronicles of the ancient mechanical beings known as Giants",
      themes: ["Giants", "Ancient Tech", "Lost Civilization"],
      bgImage: "/images/mechanical-era-bg.jpg",
    },
    {
      id: "wasteland-chronicles",
      label: "Wasteland Chronicles",
      color: "#8B8C7A", // Muted olive
      description:
        "Tales from the vast wastelands between the last human settlements",
      themes: ["Survival", "Exploration", "Ruins"],
    },
    {
      id: "giant-hunters",
      label: "Giant Hunters",
      color: "#C1666B", // Rusty red
      description:
        "Stories of those who dare to challenge the ancient mechanical titans",
      themes: ["Combat", "Strategy", "Technology"],
    },
    {
      id: "fragment-seekers",
      label: "Fragment Seekers",
      color: "#48639C", // Deep blue
      description: "Expeditions to recover lost fragments of the ancient world",
      themes: ["Discovery", "Mystery", "Power"],
    },
    {
      id: "settlement-tales",
      label: "Settlement Tales",
      color: "#E4D8B4", // Light sand
      description: "Life within the last bastions of human civilization",
      themes: ["Community", "Politics", "Survival"],
    },
  ];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="min-h-screen bg-[#1A1A1A] text-white p-8"
    >
      {/* Header */}
      <motion.div
        initial={{ y: -20 }}
        animate={{ y: 0 }}
        className="max-w-4xl mx-auto text-center mb-16"
      >
        <h1 className="text-6xl font-serif mb-4 text-[#E4D8B4]">
          SLAG Story Engine
        </h1>
        <p className="text-xl text-[#8B8C7A]">
          A single prompt to rule them all
        </p>
      </motion.div>

      {/* Genre Grid */}
      <motion.div
        className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        variants={{
          hidden: { opacity: 0 },
          show: {
            opacity: 1,
            transition: {
              staggerChildren: 0.1,
            },
          },
        }}
        initial="hidden"
        animate="show"
      >
        {genres.map((genre) => (
          <motion.button
            key={genre.id}
            onClick={() => setSelectedGenre(genre.id)}
            variants={{
              hidden: { opacity: 0, y: 20 },
              show: { opacity: 1, y: 0 },
            }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className={`
              relative p-6 rounded-xl transition-all duration-300
              bg-gradient-to-br from-black to-gray-900
              border border-opacity-30
              ${selectedGenre === genre.id ? "ring-2 ring-current" : ""}
            `}
            style={{
              borderColor: genre.color,
            }}
          >
            <div
              className="absolute inset-0 rounded-xl opacity-10"
              style={{
                background: `radial-gradient(circle at center, ${genre.color} 0%, transparent 70%)`,
              }}
            />
            <h3
              className="text-2xl font-medium mb-2 relative z-10"
              style={{ color: genre.color }}
            >
              {genre.label}
            </h3>
            <p className="text-[#8B8C7A] text-sm relative z-10">
              {genre.description}
            </p>
            <div className="flex flex-wrap gap-2 mt-4">
              {genre.themes.map((theme) => (
                <span
                  key={theme}
                  className="px-2 py-1 rounded-full text-xs"
                  style={{
                    backgroundColor: `${genre.color}20`,
                    color: genre.color,
                  }}
                >
                  {theme}
                </span>
              ))}
            </div>
          </motion.button>
        ))}
      </motion.div>

      {/* Controls */}
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="fixed bottom-8 left-1/2 -translate-x-1/2 flex items-center gap-4"
      >
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => {
            const randomIndex = Math.floor(Math.random() * genres.length);
            setSelectedGenre(genres[randomIndex].id);
          }}
          className="p-4 rounded-full bg-[#2A2A2A] hover:bg-[#3A3A3A] transition-colors border border-[#8B8C7A]"
        >
          <Shuffle className="w-6 h-6" />
        </motion.button>

        <AnimatePresence>
          {selectedGenre && (
            <motion.button
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-6 py-3 bg-[#D4B483] text-black rounded-lg hover:bg-[#E4D8B4] transition-colors flex items-center gap-2"
            >
              <Wand2 className="w-5 h-5" />
              <span>
                Generate {genres.find((g) => g.id === selectedGenre)?.label}{" "}
                Story
              </span>
            </motion.button>
          )}
        </AnimatePresence>
      </motion.div>

      {/* Genre Details Modal */}
      <AnimatePresence>
        {selectedGenre && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/90 flex items-center justify-center p-4"
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="max-w-2xl w-full bg-[#1A1A1A] rounded-2xl p-8 relative border border-[#8B8C7A]"
            >
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => setSelectedGenre(null)}
                className="absolute top-4 right-4 text-[#8B8C7A] hover:text-white"
              >
                <X className="w-6 h-6" />
              </motion.button>

              <h2
                className="text-4xl mb-4"
                style={{
                  color: genres.find((g) => g.id === selectedGenre)?.color,
                }}
              >
                {genres.find((g) => g.id === selectedGenre)?.label}
              </h2>

              <p className="text-xl text-[#8B8C7A] mb-6">
                {genres.find((g) => g.id === selectedGenre)?.description}
              </p>

              <div className="flex flex-wrap gap-2">
                {genres
                  .find((g) => g.id === selectedGenre)
                  ?.themes.map((theme) => (
                    <span
                      key={theme}
                      className="px-3 py-1 rounded-full text-sm"
                      style={{
                        backgroundColor: `${
                          genres.find((g) => g.id === selectedGenre)?.color
                        }20`,
                        color: genres.find((g) => g.id === selectedGenre)
                          ?.color,
                      }}
                    >
                      {theme}
                    </span>
                  ))}
              </div>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="mt-8 w-full py-3 bg-[#D4B483] text-black rounded-lg hover:bg-[#E4D8B4] transition-colors flex items-center justify-center gap-2"
              >
                <Wand2 className="w-5 h-5" />
                <span>Generate Story</span>
              </motion.button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

export default ExplorePage;
