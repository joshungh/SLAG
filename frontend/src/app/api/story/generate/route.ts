import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const { prompt } = await request.json();

    if (!prompt) {
      return NextResponse.json(
        { error: "Prompt is required" },
        { status: 400 }
      );
    }

    // Mock story data that matches our interface
    const mockStory = {
      bible: {
        title: "Micah's Lost Sole",
        genre: "Historical Fantasy/Comedy",
        universe: {
          setting: "Ancient Sparta and Modern Day",
          era: "Mixed - Present Day and 480 BC",
        },
        characters: [
          {
            name: "Micah Thompson",
            role: "Protagonist",
            description:
              "A modern-day teenager who accidentally time travels while searching for his lost sneaker",
            traits: null,
            background: null,
            relationships: null,
            arc: null,
          },
          {
            name: "King Leonidas",
            role: "Deuteragonist",
            description:
              "The legendary Spartan king who becomes oddly fascinated by Micah's sneaker",
            traits: null,
            background: null,
            relationships: null,
            arc: null,
          },
          {
            name: "Nike",
            role: "Supporting Character",
            description:
              "The Greek goddess of victory who's amused by the whole situation",
            traits: null,
            background: null,
            relationships: null,
            arc: null,
          },
        ],
        locations: [
          {
            name: "Modern High School",
            description: "Where Micah's adventure begins during track practice",
            significance: null,
            features: null,
            hazards: null,
            infrastructure: null,
          },
          {
            name: "Ancient Sparta",
            description:
              "The warrior city-state where Micah's shoe mysteriously appears",
            significance: null,
            features: null,
            hazards: null,
            infrastructure: null,
          },
        ],
        factions: [
          {
            name: "Spartan Warriors",
            description:
              "The elite fighting force that becomes obsessed with Micah's 'magic footwear'",
            goals: [
              "Defend Sparta",
              "Acquire the mysterious future technology (sneaker)",
            ],
            relationships: {
              "Persian Army": "Enemies",
              Micah: "Suspicious but intrigued",
            },
            resources: null,
            territory: null,
          },
        ],
        technology: [
          {
            name: "Modern Sneaker",
            description:
              "A limited edition running shoe that becomes an object of fascination in ancient Sparta",
            limitations: null,
            requirements: null,
            risks: null,
            development_stage: null,
          },
        ],
        timeline: {
          main_events: [
            {
              year: "Present Day",
              event: "The Lost Sneaker",
              details:
                "Micah loses his favorite running shoe during track practice",
              impact: null,
              key_figures: null,
            },
            {
              year: "480 BC",
              event: "Spartan Discovery",
              details:
                "The shoe mysteriously appears before King Leonidas and his army",
              impact: null,
              key_figures: null,
            },
          ],
        },
        themes: [
          "Time Travel",
          "Culture Clash",
          "Coming of Age",
          "The Value of Material Things",
        ],
        notes: [],
      },
      framework: {
        title: "Micah's Lost Sole",
        genre: "Historical Fantasy/Comedy",
        main_conflict:
          "Micah must retrieve his sneaker from the Spartan army without changing history",
        central_theme:
          "Sometimes the greatest adventures start with the smallest things",
        arcs: [],
      },
      story: {
        title: "Micah's Lost Sole",
        author: "AI Storyteller",
        genre: "Historical Fantasy/Comedy",
        content:
          "Micah Thompson had one job during track practice: don't lose his limited edition running shoes. Yet somehow, through a bizarre twist of fate (and perhaps a touch of divine intervention), one of his sneakers vanished into thin air mid-sprint.\n\nLittle did he know that at that exact moment, 2,500 years in the past, his shoe materialized in the midst of 300 Spartan warriors preparing for battle. King Leonidas himself picked up the strange footwear, marveling at its otherworldly design and impossibly light weight.\n\n'This must be a gift from the gods!' declared Leonidas, holding the sneaker aloft. His warriors gathered around, amazed by the mysterious object with its glowing reflective strips and air-cushioned sole.\n\nMeanwhile, Micah's desperate search for his shoe led him to an ancient Greek artifact in the school's history classroom. Upon touching it, he found himself transported back to 480 BC, face to face with the most fearsome warriors in history – who were now treating his lost sneaker like a sacred relic.\n\n'Um, excuse me,' Micah squeaked, 'but I think you have my shoe.'\n\nThree hundred pairs of eyes turned to stare at him. This was going to be complicated.",
        word_count: 187,
      },
      word_count: 187,
    };

    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 2000));

    return NextResponse.json(mockStory);
  } catch (error) {
    console.error("Error generating story:", error);
    return NextResponse.json(
      { error: "Failed to generate story" },
      { status: 500 }
    );
  }
}
