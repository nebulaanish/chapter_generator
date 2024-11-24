"use client";

import React from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { MinusCircle } from "lucide-react";

interface ContentItemFormProps {
  content: string;
  contentIndex: number;
  sectionIndex: number;
  updateContentItem: (
    sectionIndex: number,
    contentIndex: number,
    value: string
  ) => void;
  removeContentItem: (sectionIndex: number, contentIndex: number) => void;
}

const ContentItemForm: React.FC<ContentItemFormProps> = ({
  content,
  contentIndex,
  sectionIndex,
  updateContentItem,
  removeContentItem,
}) => {
  return (
    <div className="flex items-center gap-4">
      <Input
        value={content}
        onChange={(e) =>
          updateContentItem(sectionIndex, contentIndex, e.target.value)
        }
        placeholder="Enter content item"
      />
      <Button
        type="button"
        variant="ghost"
        size="icon"
        onClick={() => removeContentItem(sectionIndex, contentIndex)}
      >
        <MinusCircle className="h-4 w-4" />
      </Button>
    </div>
  );
};

export default ContentItemForm;
