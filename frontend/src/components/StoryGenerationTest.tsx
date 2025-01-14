import { useState, useEffect } from "react";
import GenerationProgress, { GenerationStep } from "./GenerationProgress";

const initialSteps: GenerationStep[] = [
  {
    id: "chapter_planning",
    title: "Chapter Planning",
    description: "Analyzing context and generating chapter structure",
    status: "pending",
    progress: 0,
    logs: [],
  },
  {
    id: "plot_development",
    title: "Plot Development",
    description: "Creating plot threads and character arcs",
    status: "pending",
    progress: 0,
    logs: [],
  },
  {
    id: "scene_planning",
    title: "Scene Planning",
    description: "Outlining 48 scenes across 4 acts",
    status: "pending",
    progress: 0,
    logs: [],
  },
  {
    id: "scene_generation",
    title: "Scene Generation",
    description: "Generating detailed scene content",
    status: "pending",
    progress: 0,
    logs: [],
  },
  {
    id: "continuity_check",
    title: "Continuity Check",
    description: "Validating story consistency",
    status: "pending",
    progress: 0,
    logs: [],
  },
];

// Mock API response data
const mockStoryResponse = {
  title: "The Awakening",
  chapter: 1,
  content: `The soft hum of quantum processors fills the dimly lit laboratory as Dr. James Chen leans closer to his holographic display, his weathered face illuminated by the pale blue light. The Fragment sample, suspended in the containment field before him, shouldn't be moving the way it is.

"Run sequence delta-seven again," he mumbles to himself, fingers dancing across the haptic interface. The Fragment—a crystalline shard no larger than his thumb—pulses with an internal light that defies his understanding of its composition. According to every known law of physics, it should be inert.

Six months of study, and the Fragments are still a mystery. But tonight feels different. Tonight, he's seen something new...`,
  generated_at: new Date().toISOString(),
};

const mockLogs = {
  chapter_planning: [
    "Initializing story engine...",
    "Loading previous chapter context...",
    "Analyzing active plot threads: [Initial Crisis, Fragment Discovery]",
    "Generating chapter structure with 4 acts...",
    "Chapter plan complete: The Awakening",
  ],
  plot_development: [
    "Analyzing character motivations and relationships...",
    "Developing plot thread: Fragment Anomaly",
    "Creating character arc for Dr. James Chen",
    "Establishing tension points and conflicts",
    "Plot structure finalized with 3 major threads",
  ],
  scene_planning: [
    "Designing Act 1: Laboratory Discovery",
    "Mapping character interactions and locations",
    "Creating dramatic tension curve",
    "Finalizing 48 scene outlines across 4 acts",
  ],
  scene_generation: [
    "Generating opening scene: Station Omega Lab",
    "Writing character dialogue and descriptions",
    "Building atmospheric tension",
    "Incorporating scientific elements and world-building",
  ],
  continuity_check: [
    "Validating character consistency",
    "Checking scientific accuracy",
    "Verifying plot progression",
    "Story successfully generated",
  ],
};

export default function StoryGenerationTest() {
  const [steps, setSteps] = useState<GenerationStep[]>(initialSteps);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [overallProgress, setOverallProgress] = useState(0);
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedStory, setGeneratedStory] = useState<
    typeof mockStoryResponse | null
  >(null);

  const addLogToStep = (stepId: string, message: string) => {
    setSteps((currentSteps) =>
      currentSteps.map((step) =>
        step.id === stepId
          ? {
              ...step,
              logs: [
                ...(step.logs || []),
                {
                  timestamp: new Date().toISOString(),
                  message,
                  type: "info",
                },
              ],
            }
          : step
      )
    );
  };

  const updateStepProgress = (stepId: string, progress: number) => {
    setSteps((currentSteps) =>
      currentSteps.map((step) =>
        step.id === stepId
          ? {
              ...step,
              progress,
              status: progress === 100 ? "completed" : "in_progress",
            }
          : step
      )
    );
  };

  const simulateGeneration = async () => {
    setIsGenerating(true);
    setSteps(initialSteps);
    setCurrentStepIndex(0);
    setOverallProgress(0);
    setGeneratedStory(null);

    // Simulate each step with more realistic timing
    for (let stepIndex = 0; stepIndex < steps.length; stepIndex++) {
      const step = steps[stepIndex];
      setCurrentStepIndex(stepIndex);

      // Update step status to in_progress
      setSteps((current) =>
        current.map((s, i) =>
          i === stepIndex ? { ...s, status: "in_progress" } : s
        )
      );

      // Get logs for current step
      const logs = mockLogs[step.id as keyof typeof mockLogs];

      // Simulate progress with varying speeds for different steps
      const stepDuration = stepIndex === 3 ? 8000 : 4000; // Scene generation takes longer
      const progressInterval = stepDuration / 20; // 20 updates per step

      for (let progress = 0; progress <= 100; progress += 5) {
        await new Promise((resolve) => setTimeout(resolve, progressInterval));
        updateStepProgress(step.id, progress);

        // Add logs throughout the progress
        if (logs[Math.floor((progress / 100) * logs.length)]) {
          addLogToStep(
            step.id,
            logs[Math.floor((progress / 100) * logs.length)]
          );
        }

        // Update overall progress
        const overallProgressValue =
          ((stepIndex * 100 + progress) / (steps.length * 100)) * 100;
        setOverallProgress(Math.round(overallProgressValue));
      }

      // Mark step as completed
      setSteps((current) =>
        current.map((s, i) =>
          i === stepIndex ? { ...s, status: "completed" } : s
        )
      );

      // Small pause between steps
      await new Promise((resolve) => setTimeout(resolve, 500));
    }

    // Set the generated story
    setGeneratedStory(mockStoryResponse);
    setIsGenerating(false);
  };

  return (
    <div className="p-8">
      <div className="mb-8">
        <button
          onClick={simulateGeneration}
          disabled={isGenerating}
          className={`px-6 py-3 rounded-lg font-medium text-white ${
            isGenerating
              ? "bg-gray-500 cursor-not-allowed"
              : "bg-blue-500 hover:bg-blue-600"
          }`}
        >
          {isGenerating ? "Generating Story..." : "Generate Story (Test)"}
        </button>
      </div>

      <GenerationProgress
        steps={steps}
        currentStepIndex={currentStepIndex}
        overallProgress={overallProgress}
      />

      {/* Display generated story */}
      {generatedStory && (
        <div className="mt-8 bg-black/30 rounded-lg p-6 border border-white/10">
          <h2 className="text-2xl font-bold mb-4">{generatedStory.title}</h2>
          <div className="prose prose-invert">
            {generatedStory.content.split("\n\n").map((paragraph, i) => (
              <p key={i} className="mb-4">
                {paragraph}
              </p>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
