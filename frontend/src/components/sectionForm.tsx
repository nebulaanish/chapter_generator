"use client";

import React from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Trash2, PlusCircle } from "lucide-react";
import ContentItemForm from "./contentItemForm";

interface SectionFormProps {
  section: {
    title: string;
    content: string[];
  };
  sectionIndex: number;
  updateSectionTitle: (sectionIndex: number, value: string) => void;
  addContentItem: (sectionIndex: number) => void;
  removeContentItem: (sectionIndex: number, contentIndex: number) => void;
  updateContentItem: (
    sectionIndex: number,
    contentIndex: number,
    value: string
  ) => void;
  removeSection: (sectionIndex: number) => void;
}

const SectionForm: React.FC<SectionFormProps> = ({
  section,
  sectionIndex,
  updateSectionTitle,
  addContentItem,
  removeContentItem,
  updateContentItem,
  removeSection,
}) => {
  return (
    <div className="relative">
      <div className="space-y-4">
        <div className="flex items-center gap-4">
          <Input
            value={section.title}
            onChange={(e) => updateSectionTitle(sectionIndex, e.target.value)}
            placeholder="Enter section title"
            className="font-semibold"
          />
          <Button
            type="button"
            variant="destructive"
            size="icon"
            onClick={() => removeSection(sectionIndex)}
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>

        <div className="space-y-3 pl-4">
          {section.content.map((content, contentIndex) => (
            <ContentItemForm
              key={contentIndex}
              content={content}
              contentIndex={contentIndex}
              sectionIndex={sectionIndex}
              updateContentItem={updateContentItem}
              removeContentItem={removeContentItem}
            />
          ))}

          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => addContentItem(sectionIndex)}
            className="mt-2"
          >
            <PlusCircle className="h-4 w-4 mr-2" />
            Add Content Item
          </Button>
        </div>
      </div>
    </div>
  );
};

export default SectionForm;
