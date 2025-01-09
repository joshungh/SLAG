"use client";

import { useState } from "react";
import { Switch } from "@/components/ui/switch";
import {
  BookOpen,
  Settings2,
  Sparkles,
  Brain,
  Globe,
  Info,
  Layers,
  FileText,
} from "lucide-react";

interface StorySettings {
  // Phase 1: Story Bible Settings
  genre: string[];
  worldBuilding: {
    characters: boolean;
    locations: boolean;
    lore: boolean;
    technology: boolean;
    fragments: boolean; // For SLAG-specific lore
    giants: boolean; // For mechanical-sentient beings
  };
  timelinePlacement: "pre-fragment" | "post-fragment" | "current-era";
  location: string[];

  // Phase 2: Story Arc Settings
  structure: "three-act" | "five-act" | "hero-journey";
  length: "short" | "medium" | "long";
  chapters: number;
  subplots: number;
  aiIntegration: {
    claude: boolean;
    titan: boolean;
  };

  // Phase 3: Narrative Settings
  pov: "first" | "third" | "omniscient";
  targetAudience: string;
  tone: string[];
  narrativeStyle: string[];
  artStyle: string[];
}

export default function CreatePage() {
  const [currentPhase, setCurrentPhase] = useState<1 | 2 | 3>(1);
  const [prompt, setPrompt] = useState("");
  const [isAdvancedMode, setIsAdvancedMode] = useState(false);
  const [settings, setSettings] = useState<StorySettings>({
    // Phase 1 defaults
    genre: [],
    worldBuilding: {
      characters: true,
      locations: true,
      lore: true,
      technology: false,
      fragments: false,
      giants: false,
    },
    timelinePlacement: "current-era",
    location: [],

    // Phase 2 defaults
    structure: "three-act",
    length: "medium",
    chapters: 5,
    subplots: 2,
    aiIntegration: {
      claude: false,
      titan: false,
    },

    // Phase 3 defaults
    pov: "third",
    targetAudience: "young-adult",
    tone: [],
    narrativeStyle: [],
    artStyle: [],
  });

  const defaultGenres = [
    "Sci-Fi",
    "Mecha",
    "Post-Apocalyptic",
    "Space Opera",
    "Cyberpunk",
    "Military SF",
  ];

  const defaultLocations = [
    "Station Omega",
    "Fragment Research Zone",
    "Giant Ruins",
    "Abandoned Megastructures",
    "Underground Facilities",
  ];

  const PhaseIndicator = () => (
    <div className="flex items-center space-x-2 mb-8">
      {[1, 2, 3].map((phase) => (
        <button
          key={phase}
          onClick={() => setCurrentPhase(phase as 1 | 2 | 3)}
          className={`flex items-center space-x-2 px-4 py-2 rounded-lg ${
            currentPhase === phase
              ? "bg-green-400 text-black"
              : "bg-gray-800 text-gray-400"
          }`}
        >
          {phase === 1 && <Globe className="w-4 h-4" />}
          {phase === 2 && <Layers className="w-4 h-4" />}
          {phase === 3 && <FileText className="w-4 h-4" />}
          <span>Phase {phase}</span>
        </button>
      ))}
    </div>
  );

  const renderPhaseContent = () => {
    switch (currentPhase) {
      case 1:
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-medium">Story Bible Creation</h2>

            {/* Genre Selection */}
            <div>
              <label className="text-lg font-medium mb-2 block">
                Genre Mix
              </label>
              <div className="flex flex-wrap gap-2">
                {defaultGenres.map((genre) => (
                  <button
                    key={genre}
                    className={`px-3 py-1.5 rounded-full text-sm ${
                      settings.genre.includes(genre)
                        ? "bg-green-400 text-black"
                        : "bg-gray-800 text-gray-300 hover:bg-gray-700"
                    }`}
                    onClick={() => toggleGenre(genre)}
                  >
                    {genre}
                  </button>
                ))}
              </div>
            </div>

            {/* Location Selection */}
            <div>
              <label className="text-lg font-medium mb-2 block">
                Primary Location
              </label>
              <div className="flex flex-wrap gap-2">
                {defaultLocations.map((loc) => (
                  <button
                    key={loc}
                    className={`px-3 py-1.5 rounded-full text-sm ${
                      settings.location.includes(loc)
                        ? "bg-green-400 text-black"
                        : "bg-gray-800 text-gray-300 hover:bg-gray-700"
                    }`}
                    onClick={() => toggleLocation(loc)}
                  >
                    {loc}
                  </button>
                ))}
              </div>
            </div>

            {/* World Building Options */}
            <div className="grid grid-cols-2 gap-4">
              {Object.entries(settings.worldBuilding).map(([key, value]) => (
                <div
                  key={key}
                  className="flex items-center justify-between p-4 bg-gray-900/50 rounded-lg"
                >
                  <span className="capitalize">{key}</span>
                  <Switch
                    checked={value}
                    onCheckedChange={(checked) =>
                      setSettings({
                        ...settings,
                        worldBuilding: {
                          ...settings.worldBuilding,
                          [key]: checked,
                        },
                      })
                    }
                  />
                </div>
              ))}
            </div>

            {/* Timeline Placement */}
            <div>
              <label className="text-lg font-medium mb-2 block">
                Timeline Era
              </label>
              <select
                className="w-full bg-gray-800 rounded-lg px-4 py-2 text-white"
                value={settings.timelinePlacement}
                onChange={(e) =>
                  setSettings({
                    ...settings,
                    timelinePlacement: e.target.value as any,
                  })
                }
              >
                <option value="pre-fragment">Pre-Fragment Era</option>
                <option value="post-fragment">Post-Fragment Era</option>
                <option value="current-era">Current Era (4424 CE)</option>
              </select>
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-medium">Story Arc Development</h2>
            {/* Story Structure Options */}
            <div>
              <label className="text-lg font-medium mb-2 block">
                Story Structure
              </label>
              <select className="w-full bg-gray-800 rounded-lg px-4 py-2 text-white">
                <option value="three-act">Three Act Structure</option>
                <option value="five-act">Five Act Structure</option>
                <option value="hero-journey">Hero's Journey</option>
              </select>
            </div>
            {/* Chapter and Subplot Controls */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-lg font-medium mb-2 block">
                  Number of Chapters
                </label>
                <input
                  type="number"
                  min={1}
                  max={20}
                  value={settings.chapters}
                  onChange={(e) =>
                    setSettings({ ...settings, chapters: +e.target.value })
                  }
                  className="w-full bg-gray-800 rounded-lg px-4 py-2 text-white"
                />
              </div>
              <div>
                <label className="text-lg font-medium mb-2 block">
                  Number of Subplots
                </label>
                <input
                  type="number"
                  min={0}
                  max={5}
                  value={settings.subplots}
                  onChange={(e) =>
                    setSettings({ ...settings, subplots: +e.target.value })
                  }
                  className="w-full bg-gray-800 rounded-lg px-4 py-2 text-white"
                />
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-6">
            <h2 className="text-xl font-medium">Narrative Generation</h2>
            {/* Narrative Settings */}
            <div className="space-y-6">
              {/* Point of View Selection */}
              <div>
                <label className="text-lg font-medium mb-2 block">
                  Point of View
                </label>
                <div className="flex space-x-4">
                  {["First Person", "Third Person", "Omniscient"].map((pov) => (
                    <button
                      key={pov}
                      className="px-4 py-2 rounded-lg bg-gray-800 text-gray-300 hover:bg-gray-700"
                    >
                      {pov}
                    </button>
                  ))}
                </div>
              </div>
              {/* Target Audience */}
              <div>
                <label className="text-lg font-medium mb-2 block">
                  Target Audience
                </label>
                <select className="w-full bg-gray-800 rounded-lg px-4 py-2 text-white">
                  <option value="children">Children</option>
                  <option value="middle-grade">Middle Grade</option>
                  <option value="young-adult">Young Adult</option>
                  <option value="adult">Adult</option>
                </select>
              </div>
            </div>
          </div>
        );
    }
  };

  // Helper functions
  const toggleGenre = (genre: string) => {
    setSettings({
      ...settings,
      genre: settings.genre.includes(genre)
        ? settings.genre.filter((g) => g !== genre)
        : [...settings.genre, genre],
    });
  };

  const toggleLocation = (location: string) => {
    setSettings({
      ...settings,
      location: settings.location.includes(location)
        ? settings.location.filter((l) => l !== location)
        : [...settings.location, location],
    });
  };

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-4xl mx-auto p-6">
        {/* Mode Toggle and Settings */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center space-x-4">
            <Switch
              checked={isAdvancedMode}
              onCheckedChange={setIsAdvancedMode}
              className="data-[state=checked]:bg-green-400"
            />
            <div className="flex items-center space-x-2">
              {isAdvancedMode ? (
                <Settings2 className="w-5 h-5 text-green-400" />
              ) : (
                <Sparkles className="w-5 h-5 text-green-400" />
              )}
              <span className="text-lg font-medium">
                {isAdvancedMode ? "Advanced Mode" : "Basic Mode"}
              </span>
            </div>
          </div>
          <button className="text-gray-400 hover:text-white flex items-center space-x-1">
            <Brain className="w-5 h-5" />
            <span>Brainstorm Ideas</span>
          </button>
        </div>

        {/* Phase Indicator */}
        {isAdvancedMode && <PhaseIndicator />}

        {/* Main Input Area */}
        <div className="space-y-6">
          {/* Prompt Input */}
          <div className="relative">
            <div className="flex items-center space-x-2 mb-2">
              <span className="text-lg font-medium">Story Prompt</span>
              <Info className="w-4 h-4 text-gray-400" />
            </div>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Enter your story prompt here..."
              className="w-full h-32 bg-gray-900/50 rounded-lg p-4 text-white placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-green-400/50 resize-none"
            />
            <div className="absolute bottom-4 right-4 text-sm text-gray-500">
              {prompt.length} / 3000
            </div>
          </div>

          {/* Advanced Settings */}
          {isAdvancedMode && renderPhaseContent()}

          {/* Generate Button */}
          <button className="w-full bg-green-400 text-black py-3 rounded-lg font-medium hover:bg-green-300 transition-colors flex items-center justify-center space-x-2">
            <BookOpen className="w-5 h-5" />
            <span>
              {isAdvancedMode
                ? `Generate Phase ${currentPhase}`
                : "Generate Story"}
            </span>
          </button>
        </div>
      </div>
    </div>
  );
}
