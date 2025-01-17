"use client";

import { useState } from "react";
import { Trash2, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";

interface DeleteStoryButtonProps {
  storyId: string;
  onDelete: (id: string) => Promise<void>;
  variant?: "icon" | "default";
}

export function DeleteStoryButton({
  storyId,
  onDelete,
  variant = "icon",
}: DeleteStoryButtonProps) {
  const [isDeleting, setIsDeleting] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const handleDelete = async () => {
    if (!showConfirm) {
      setShowConfirm(true);
      return;
    }

    try {
      setIsDeleting(true);
      await onDelete(storyId);
    } catch (error) {
      console.error("Failed to delete story:", error);
    } finally {
      setIsDeleting(false);
      setShowConfirm(false);
    }
  };

  if (variant === "icon") {
    return (
      <Button
        variant="ghost"
        size="icon"
        onClick={handleDelete}
        disabled={isDeleting}
        title={showConfirm ? "Click again to confirm deletion" : "Delete story"}
      >
        {isDeleting ? (
          <Loader2 className="h-4 w-4 animate-spin text-muted-foreground" />
        ) : (
          <Trash2
            className={`h-4 w-4 ${
              showConfirm ? "text-destructive" : "text-muted-foreground"
            }`}
          />
        )}
      </Button>
    );
  }

  return (
    <Button
      variant="destructive"
      onClick={handleDelete}
      disabled={isDeleting}
      className="w-full"
    >
      {isDeleting ? (
        <>
          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
          Deleting...
        </>
      ) : (
        <>
          <Trash2 className="mr-2 h-4 w-4" />
          {showConfirm ? "Click again to confirm" : "Delete Story"}
        </>
      )}
    </Button>
  );
}
