"use client";

import React from "react";
import { Input } from "@/components/ui/input";

interface SourceFormProps {
  source: string;
  sourceType: string;
  setSource: (value: string) => void;
  setSourceType: (value: string) => void;
}

const SourceForm: React.FC<SourceFormProps> = ({
  source,
  sourceType,
  setSource,
  setSourceType,
}) => {
  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-1">Source URL</label>
        <Input
          value={source}
          onChange={(e) => setSource(e.target.value)}
          className="w-full"
          placeholder="Enter source URL"
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Source Type</label>
        <select
          value={sourceType}
          onChange={(e) => setSourceType(e.target.value)}
        >
          <option value="url">url</option>
          <option value="pdf">pdf</option>
        </select>
      </div>
    </div>
  );
};

export default SourceForm;
