"use client";

import FileUpload from "@/components/form/fileUpload";
import ResponseTypeSelector from "@/components/form/responseTypeSelector";
import TopicOutline from "@/components/form/topicOutline";
import URLInput from "@/components/form/urlInput";
import { useState } from "react";

interface Topic {
  topic: string;
  outlines: string;
}

interface FormData {
  file: File | null;
  url: string;
  topics: Topic[];
  responseType: string;
}

export default function Home() {
  const [formData, setFormData] = useState<FormData>({
    file: null,
    url: "",
    topics: [{ topic: "", outlines: "" }],
    responseType: "profession",
  });

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log("Form Data Submitted: ", formData);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center">
      <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-2xl">
        <h1 className="text-2xl font-bold mb-6">Chapter Generator</h1>
        <form onSubmit={handleSubmit} className="space-y-6">
          <FileUpload formData={formData} setFormData={setFormData} />
          <URLInput formData={formData} setFormData={setFormData} />
          <TopicOutline formData={formData} setFormData={setFormData} />
          <ResponseTypeSelector formData={formData} setFormData={setFormData} />
          <button
            type="submit"
            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition"
          >
            Submit
          </button>
        </form>
      </div>
    </div>
  );
}
