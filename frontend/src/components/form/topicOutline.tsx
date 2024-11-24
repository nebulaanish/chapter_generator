interface Topic {
  topic: string;
  outlines: string;
}

interface Props {
  formData: { topics: Topic[] };
  setFormData: React.Dispatch<React.SetStateAction<any>>;
}

export default function TopicOutline({ formData, setFormData }: Props) {
  const handleChange = (index: number, field: keyof Topic, value: string) => {
    const updatedTopics = formData.topics.map((item, idx) =>
      idx === index ? { ...item, [field]: value } : item
    );
    setFormData({ ...formData, topics: updatedTopics });
  };

  const addTopic = () => {
    setFormData({
      ...formData,
      topics: [...formData.topics, { topic: "", outlines: "" }],
    });
  };

  const removeTopic = (index: number) => {
    const updatedTopics = formData.topics.filter((_, idx) => idx !== index);
    setFormData({ ...formData, topics: updatedTopics });
  };

  return (
    <div className="p-4 bg-gray-100 rounded-md shadow-md">
      <label className="block text-lg font-semibold mb-4 text-gray-800">
        Topics and Outlines
      </label>
      {formData.topics.map((item, index) => (
        <div
          key={index}
          className="mb-6 p-4 border rounded-md bg-white shadow-sm relative"
        >
          <div className="mb-3">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Topic {index + 1}
            </label>
            <input
              type="text"
              value={item.topic}
              onChange={(e) => handleChange(index, "topic", e.target.value)}
              placeholder={`Enter topic ${index + 1}`}
              className="block w-full text-sm border-gray-300 rounded-md py-2 px-3 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Outlines
            </label>
            <textarea
              value={item.outlines}
              onChange={(e) => handleChange(index, "outlines", e.target.value)}
              placeholder="Enter the outlines"
              rows={4}
              className="block w-full text-sm border-gray-300 rounded-md px-3 py-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          {formData.topics.length > 1 && (
            <button
              type="button"
              onClick={() => removeTopic(index)}
              className="absolute top-1 right-4 bg-red-500 text-white py-1 px-3 rounded hover:bg-red-600 transition"
            >
              Remove
            </button>
          )}
        </div>
      ))}
      <button
        type="button"
        onClick={addTopic}
        className="mt-4 bg-green-500 text-white px-6 py-2 rounded hover:bg-green-600 transition"
      >
        + Add Topic
      </button>
    </div>
  );
}
