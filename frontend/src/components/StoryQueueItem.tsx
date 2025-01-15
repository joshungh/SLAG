interface StoryQueueItemProps {
  id: string;
  prompt: string;
  status: string;
}

export default function StoryQueueItem({
  prompt,
  status,
}: StoryQueueItemProps) {
  return (
    <div className="flex items-center justify-between py-2 px-3 rounded-lg bg-black/20 border border-gray-800">
      <div className="flex items-center space-x-2">
        <div
          className={`w-2 h-2 rounded-full ${
            status === "generating"
              ? "bg-blue-500 animate-pulse"
              : status === "completed"
              ? "bg-green-500"
              : status === "error"
              ? "bg-red-500"
              : "bg-gray-500"
          }`}
        />
        <span className="text-sm text-gray-400 truncate max-w-[300px] sm:max-w-[400px]">
          {prompt}
        </span>
      </div>
      <span className="text-xs text-gray-500 capitalize">{status}</span>
    </div>
  );
}
