export interface Step {
  id: string;
  title: string;
  status: "pending" | "in-progress" | "completed";
}

export const GENERATION_STEPS: Step[] = [
  {
    id: "world-genesis",
    title: "World Building",
    status: "pending",
  },
  {
    id: "story-bible",
    title: "Story Bible",
    status: "pending",
  },
  {
    id: "outline",
    title: "Story Outline",
    status: "pending",
  },
  {
    id: "scene-drafts",
    title: "Scene Writing",
    status: "pending",
  },
  {
    id: "final-assembly",
    title: "Final Polish",
    status: "pending",
  },
];
