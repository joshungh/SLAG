"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Wand2 } from "lucide-react";
import GenerationProgress, {
  GenerationStep,
} from "@/components/GenerationProgress";
import { useWeb3 } from "../../../contexts/Web3Context";
import StoryGenerationTest from "@/components/StoryGenerationTest";

interface StoryResponse {
  bible: {
    title: string;
    genre: string;
    universe: {
      setting: string;
      era: string;
    };
    characters: Array<{
      name: string;
      role: string;
      description: string;
      traits: any;
      background: any;
      relationships: any;
      arc: any;
    }>;
    locations: Array<{
      name: string;
      description: string;
      significance: any;
      features: any;
      hazards: any;
      infrastructure: any;
    }>;
    factions: Array<{
      name: string;
      description: string;
      goals: string[];
      relationships: Record<string, string>;
      resources: any;
      territory: any;
    }>;
    technology: Array<{
      name: string;
      description: string;
      limitations: any;
      requirements: any;
      risks: any;
      development_stage: any;
    }>;
    timeline: {
      main_events: Array<{
        year: string;
        event: string;
        details: string;
        impact: any;
        key_figures: any;
      }>;
    };
    themes: string[];
    notes: string[];
  };
  framework: {
    title: string;
    genre: string;
    main_conflict: string;
    central_theme: string;
    arcs: Array<{
      name: string;
      description: string;
      beats: Array<{
        name: string;
        description: string;
        characters_involved: string[];
        location: string;
        purpose: string;
        conflict_type: string;
        resolution_type: string;
      }>;
      themes: string[];
      character_arcs: Record<string, string>;
    }>;
  };
  story: {
    title: string;
    author: string;
    genre: string;
    content: string;
    word_count: number;
  };
  word_count: number;
}

export default function CreatePage() {
  const { connected, publicKey } = useWeb3();
  const [prompt, setPrompt] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [overallProgress, setOverallProgress] = useState(0);
  // Commented out for testing
  // const [freePromptsUsed, setFreePromptsUsed] = useState(0);
  const [generatedStory, setGeneratedStory] = useState<StoryResponse | null>(
    null
  );
  const [error, setError] = useState<string | null>(null);
  const [showCursor, setShowCursor] = useState(true);

  // Commented out for testing
  /* useEffect(() => {
    if (publicKey) {
      const storedPrompts = localStorage.getItem(`freePrompts_${publicKey}`);
      if (storedPrompts) {
        setFreePromptsUsed(parseInt(storedPrompts));
      } else {
        setFreePromptsUsed(0);
      }
    }
  }, [publicKey]); */

  // Add cursor blink effect
  useEffect(() => {
    const interval = setInterval(() => {
      setShowCursor((prev) => !prev);
    }, 530);
    return () => clearInterval(interval);
  }, []);

  const steps: GenerationStep[] = [
    {
      id: "prompt",
      title: "Analyzing Prompt",
      description: "Processing your story idea and extracting key elements",
      status: "pending",
      estimatedTime: "30s",
    },
    {
      id: "generation",
      title: "Generating Story",
      description: "Creating your unique story with characters and plot",
      status: "pending",
      estimatedTime: "1m",
    },
  ];

  const startGeneration = async () => {
    if (!connected) {
      setError("Please connect your wallet to generate stories");
      return;
    }

    if (!prompt.trim()) {
      setError("Please enter a prompt first");
      return;
    }

    setError(null);
    setIsGenerating(true);
    setCurrentStepIndex(0);
    setOverallProgress(0);

    // TEMPORARILY USING TEST VERSION
    // Comment out the real API call
    /*
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30 * 60 * 1000); // 30 minute timeout

    try {
      // Make API call to generate story
      const response = await fetch(
        "http://vmini-engine-alb-production-943444221.us-west-2.elb.amazonaws.com/generate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ prompt }),
          signal: controller.signal,
          // Increase timeouts
          keepalive: true,
        }
      );

      if (!response.ok) {
        throw new Error(
          `Failed to generate story: ${response.status} ${response.statusText}`
        );
      }

      // Start reading the response as a stream
      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error("Failed to read response stream");
      }

      let story = "";
      let decoder = new TextDecoder();

      // Mark first step as completed
      steps[0].status = "completed";
      steps[0].progress = 100;
      setCurrentStepIndex(1);
      setOverallProgress(50);

      // Start second step
      steps[1].status = "in_progress";
      steps[1].progress = 0;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        // Decode the chunk and append to story
        const chunk = decoder.decode(value);
        story += chunk;

        // Update progress based on the log messages in the chunk
        if (chunk.includes("Analyzing prompt")) {
          steps[1].progress = 20;
        } else if (chunk.includes("Generating framework")) {
          steps[1].progress = 40;
        } else if (chunk.includes("Creating story bible")) {
          steps[1].progress = 60;
        } else if (chunk.includes("Writing story")) {
          steps[1].progress = 80;
        }

        setOverallProgress(50 + Math.floor((steps[1].progress || 0) / 2));
      }

      // Parse the complete story response
      const data = JSON.parse(story);

      // Mark second step as completed
      steps[1].status = "completed";
      steps[1].progress = 100;
      setOverallProgress(100);

      setGeneratedStory(data);
    } catch (err) {
      console.error("Error generating story:", err);
      steps[currentStepIndex].status = "error";
      if (err.name === "AbortError") {
        setError("Story generation timed out. Please try again.");
      } else {
        setError("Failed to generate story. Please try again.");
      }
    } finally {
      clearTimeout(timeoutId);
      setIsGenerating(false);
    }
    */

    // Use test version instead
    try {
      // Simulate API delay
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // Use our test component's mock data
      const mockResponse: StoryResponse = {
        bible: {
          title: "The Awakening",
          genre: "Science Fiction",
          universe: {
            setting: "Station Omega",
            era: "Near Future",
          },
          characters: [
            {
              name: "Dr. James Chen",
              role: "Protagonist",
              description:
                "A dedicated scientist studying mysterious Fragment artifacts",
              traits: null,
              background: null,
              relationships: null,
              arc: null,
            },
          ],
          locations: [
            {
              name: "Station Omega Lab",
              description:
                "A high-tech research facility where Fragments are studied",
              significance: null,
              features: null,
              hazards: null,
              infrastructure: null,
            },
          ],
          themes: ["Discovery", "Scientific Mystery", "Ancient Technology"],
          notes: [],
          factions: [],
          technology: [],
          timeline: {
            main_events: [],
          },
        },
        framework: {
          title: "The Awakening",
          genre: "Science Fiction",
          main_conflict:
            "A scientist discovers an anomaly in ancient artifacts",
          central_theme: "Scientific discovery and mystery",
          arcs: [],
        },
        story: {
          title: "The Awakening",
          author: "SLAG AI",
          genre: "Science Fiction",
          content: `The soft hum of quantum processors fills the dimly lit laboratory as Dr. James Chen leans closer to his holographic display, his weathered face illuminated by the pale blue light. The Fragment sample, suspended in the containment field before him, shouldn't be moving the way it is.

"Run sequence delta-seven again," he mumbles to himself, fingers dancing across the haptic interface. The Fragment—a crystalline shard no larger than his thumb—pulses with an internal light that defies his understanding of its composition. According to every known law of physics, it should be inert.

Six months of study, and the Fragments are still a mystery. But tonight feels different. Tonight, he's seen something new...`,
          word_count: 187,
        },
        word_count: 187,
      };

      // Mark first step as completed
      steps[0].status = "completed";
      steps[0].progress = 100;
      setCurrentStepIndex(1);
      setOverallProgress(50);

      // Simulate second step progress
      steps[1].status = "in_progress";
      for (let progress = 0; progress <= 100; progress += 10) {
        steps[1].progress = progress;
        setOverallProgress(50 + Math.floor(progress / 2));
        await new Promise((resolve) => setTimeout(resolve, 300));
      }

      // Mark second step as completed
      steps[1].status = "completed";
      steps[1].progress = 100;
      setOverallProgress(100);

      setGeneratedStory(mockResponse);
    } catch (err) {
      console.error("Error in test generation:", err);
      steps[currentStepIndex].status = "error";
      setError("Failed to generate story. Please try again.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="max-w-2xl mx-auto space-y-8">
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold">Create Your Story</h1>
          {/* Commented out for testing
          {connected && (
            <div className="bg-black/30 rounded-lg p-4">
              <p className="text-gray-400">
                {3 - freePromptsUsed} free{" "}
                {3 - freePromptsUsed === 1 ? "prompt" : "prompts"} remaining
              </p>
            </div>
          )} */}
        </div>

        <div className="space-y-4">
          <div className="relative">
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              className="w-full h-32 px-4 py-3 rounded-lg bg-black/50 border border-gray-700 focus:border-green-500 focus:ring-1 focus:ring-green-500 transition-colors text-green-400 font-['IBM_Plex_Mono'] text-base tracking-tight"
              disabled={isGenerating || !connected}
            />
            <div
              className="absolute pointer-events-none select-none"
              style={{
                top: "12px",
                left: "16px",
                right: "16px",
                opacity: prompt ? 0 : 1,
              }}
            >
              <span className="font-['IBM_Plex_Mono'] text-lg tracking-tight text-gray-500">
                Enter your story idea...
                <span
                  className={`text-green-400 ${
                    showCursor ? "opacity-100" : "opacity-0"
                  }`}
                >
                  ▋
                </span>
              </span>
            </div>
          </div>

          {error && (
            <div className="bg-red-500/10 border border-red-500 text-red-400 text-sm p-3 rounded-lg">
              {error}
            </div>
          )}

          <div className="relative group">
            <button
              onClick={startGeneration}
              disabled={
                isGenerating || !connected /* || freePromptsUsed >= 3 */
              }
              className="w-full py-3 px-4 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 rounded-lg font-medium flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-white"
            >
              <Wand2 className="w-5 h-5" />
              <span>{isGenerating ? "Generating..." : "Generate Story"}</span>
            </button>
            {!connected && (
              <div className="absolute -top-12 left-1/2 -translate-x-1/2 w-max opacity-0 group-hover:opacity-100 transition-opacity bg-black/90 text-white text-sm py-2 px-3 rounded pointer-events-none">
                Connect your wallet to generate stories
              </div>
            )}
          </div>
        </div>

        {isGenerating && (
          <GenerationProgress
            steps={steps}
            currentStepIndex={currentStepIndex}
            overallProgress={overallProgress}
          />
        )}

        {generatedStory && !isGenerating && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-black/50 rounded-lg p-6 space-y-8"
          >
            <div className="flex justify-between items-center">
              <h2 className="text-2xl font-bold">
                {generatedStory?.bible?.title || "Generated Story"}
              </h2>
              <button
                onClick={() => {
                  const element = document.createElement("a");
                  const file = new Blob(
                    [JSON.stringify(generatedStory, null, 2)],
                    {
                      type: "application/json",
                    }
                  );
                  element.href = URL.createObjectURL(file);
                  element.download = `${(
                    generatedStory?.bible?.title || "story"
                  )
                    .toLowerCase()
                    .replace(/\s+/g, "_")}.json`;
                  document.body.appendChild(element);
                  element.click();
                  document.body.removeChild(element);
                }}
                className="px-4 py-2 bg-green-500 hover:bg-green-600 rounded-lg text-white flex items-center space-x-2 transition-colors"
              >
                <span>Download Story</span>
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <h3 className="text-lg font-medium mb-2">Genre</h3>
                <p className="text-gray-400">
                  {generatedStory?.bible?.genre || "Unknown"}
                </p>
              </div>
              <div>
                <h3 className="text-lg font-medium mb-2">Setting</h3>
                <p className="text-gray-400">
                  {generatedStory?.bible?.universe?.setting || "Unknown"}
                </p>
                <p className="text-gray-400 mt-1">
                  {generatedStory?.bible?.universe?.era || "Unknown"}
                </p>
              </div>
            </div>

            {generatedStory?.bible?.characters?.length > 0 && (
              <div>
                <h3 className="text-lg font-medium mb-2">Characters</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {generatedStory.bible.characters.map((character, index) => (
                    <div key={index} className="bg-black/30 rounded p-3">
                      <div className="font-medium text-green-400">
                        {character.name}
                      </div>
                      <div className="text-sm text-gray-400">
                        {character.role}
                      </div>
                      <div className="text-sm mt-1">
                        {character.description}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {generatedStory?.bible?.locations?.length > 0 && (
              <div>
                <h3 className="text-lg font-medium mb-2">Locations</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {generatedStory.bible.locations.map((location, index) => (
                    <div key={index} className="bg-black/30 rounded p-3">
                      <div className="font-medium text-green-400">
                        {location.name}
                      </div>
                      <div className="text-sm mt-1">{location.description}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {generatedStory?.bible?.factions?.length > 0 && (
              <div>
                <h3 className="text-lg font-medium mb-2">Factions</h3>
                <div className="grid grid-cols-1 gap-3">
                  {generatedStory.bible.factions.map((faction, index) => (
                    <div key={index} className="bg-black/30 rounded p-3">
                      <div className="font-medium text-green-400">
                        {faction.name}
                      </div>
                      <div className="text-sm mt-1">{faction.description}</div>
                      {faction.goals?.length > 0 && (
                        <div className="mt-2">
                          <div className="text-sm font-medium mb-1">Goals:</div>
                          <ul className="list-disc list-inside text-sm text-gray-400">
                            {faction.goals.map((goal, idx) => (
                              <li key={idx}>{goal}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {generatedStory?.bible?.technology?.length > 0 && (
              <div>
                <h3 className="text-lg font-medium mb-2">Technology</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {generatedStory.bible.technology.map((tech, index) => (
                    <div key={index} className="bg-black/30 rounded p-3">
                      <div className="font-medium text-green-400">
                        {tech.name}
                      </div>
                      <div className="text-sm mt-1">{tech.description}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {generatedStory?.bible?.timeline?.main_events?.length > 0 && (
              <div>
                <h3 className="text-lg font-medium mb-2">Timeline</h3>
                <div className="space-y-3">
                  {generatedStory.bible.timeline.main_events.map(
                    (event, index) => (
                      <div key={index} className="bg-black/30 rounded p-3">
                        <div className="font-medium text-green-400">
                          {event.year}
                        </div>
                        <div className="text-sm font-medium">{event.event}</div>
                        <div className="text-sm text-gray-400 mt-1">
                          {event.details}
                        </div>
                      </div>
                    )
                  )}
                </div>
              </div>
            )}

            {generatedStory?.bible?.themes?.length > 0 && (
              <div>
                <h3 className="text-lg font-medium mb-2">Themes</h3>
                <div className="flex flex-wrap gap-2">
                  {generatedStory.bible.themes.map((theme, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-green-500/10 border border-green-500/20 rounded-full text-sm text-green-400"
                    >
                      {theme}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {generatedStory?.story?.content && (
              <div>
                <h3 className="text-lg font-medium mb-2">Story</h3>
                <div className="bg-black/30 rounded-lg p-4">
                  <div className="prose prose-invert max-w-none">
                    {generatedStory.story.content
                      .split("\n\n")
                      .map((paragraph, index) => (
                        <p key={index} className="mb-4 last:mb-0">
                          {paragraph}
                        </p>
                      ))}
                  </div>
                </div>
                {generatedStory.story.word_count && (
                  <div className="mt-2 text-sm text-gray-400">
                    Word count: {generatedStory.story.word_count}
                  </div>
                )}
              </div>
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
}
