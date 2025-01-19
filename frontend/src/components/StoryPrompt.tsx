import { useState, useEffect } from "react";

interface StoryPromptProps {
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export default function StoryPrompt({
  value,
  onChange,
  disabled = false,
}: StoryPromptProps) {
  const [showCursor, setShowCursor] = useState(true);

  // Cursor blink effect with cleanup
  useEffect(() => {
    const interval = setInterval(() => {
      setShowCursor((prev) => !prev);
    }, 500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative group">
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full h-32 sm:h-40 px-4 py-3 rounded-xl bg-black/50 border border-gray-800 group-hover:border-green-500/50 focus:border-green-500 focus:ring-1 focus:ring-green-500 transition-all text-green-400 font-['IBM_Plex_Mono'] text-sm sm:text-base tracking-tight resize-none"
        disabled={disabled}
      />
      <div
        className="absolute pointer-events-none select-none"
        style={{
          top: "12px",
          left: "16px",
          right: "16px",
          opacity: value ? 0 : 1,
        }}
      >
        <span className="font-['IBM_Plex_Mono'] text-base sm:text-lg tracking-tight text-gray-500">
          Enter your story idea...
          <span
            className={`text-green-400 ${
              showCursor ? "opacity-100" : "opacity-0"
            } transition-opacity`}
          >
            ▋
          </span>
        </span>
      </div>
    </div>
  );
}
