"use client";

import React, { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import SectionForm from "./sectionForm";
import SourceForm from "./sourceForm";

const CourseOutlineForm: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [source, setSource] = useState("");
  const [sourceType, setSourceType] = useState("");
  const [sections, setSections] = useState([{ title: "", content: [""] }]);
  const [responseData, setResponseData] = useState<any>(null); // State to store response

  const addSection = () =>
    setSections([...sections, { title: "", content: [""] }]);
  const removeSection = (sectionIndex: number) =>
    setSections(sections.filter((_, index) => index !== sectionIndex));

  const updateSectionTitle = (sectionIndex: number, value: string) => {
    const newSections = [...sections];
    newSections[sectionIndex].title = value;
    setSections(newSections);
  };

  const addContentItem = (sectionIndex: number) => {
    const newSections = [...sections];
    newSections[sectionIndex].content.push("");
    setSections(newSections);
  };

  const removeContentItem = (sectionIndex: number, contentIndex: number) => {
    const newSections = [...sections];
    newSections[sectionIndex].content = newSections[
      sectionIndex
    ].content.filter((_, index) => index !== contentIndex);
    setSections(newSections);
  };

  const updateContentItem = (
    sectionIndex: number,
    contentIndex: number,
    value: string
  ) => {
    const newSections = [...sections];
    newSections[sectionIndex].content[contentIndex] = value;
    setSections(newSections);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    const payload = {
      source,
      source_type: sourceType,
      course_outline: sections,
    };

    try {
      const response = await fetch(
        "http://localhost:8000/api/chapters/generate/",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        }
      );

      console.log("Response object:", response);

      if (!response.ok) throw new Error("Failed to submit course outline");

      const responseData = await response.json();
      console.log("Response data:", responseData);
      setResponseData(responseData); // Save response data in state

      alert("Course outline submitted successfully!");
    } catch (error) {
      alert(
        "Error: " + (error instanceof Error ? error.message : "Unknown error")
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <form onSubmit={handleSubmit}>
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Create Course Outline</CardTitle>
          </CardHeader>
          <CardContent>
            <SourceForm
              source={source}
              sourceType={sourceType}
              setSource={setSource}
              setSourceType={setSourceType}
            />
          </CardContent>
        </Card>

        <div className="space-y-6">
          {sections.map((section, index) => (
            <SectionForm
              key={index}
              section={section}
              sectionIndex={index}
              updateSectionTitle={updateSectionTitle}
              addContentItem={addContentItem}
              removeContentItem={removeContentItem}
              updateContentItem={updateContentItem}
              removeSection={removeSection}
            />
          ))}

          <Button
            type="button"
            variant="outline"
            onClick={addSection}
            className="w-full"
          >
            Add New Section
          </Button>

          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? "Submitting..." : "Submit Course Outline"}
          </Button>
        </div>
      </form>

      {responseData && (
        <div className="mt-6">
          <h2 className="text-xl font-bold mb-4">Generated Response</h2>
          <Card>
            <CardHeader>
              <CardTitle>{responseData.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <p>{responseData.text}</p>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default CourseOutlineForm;
