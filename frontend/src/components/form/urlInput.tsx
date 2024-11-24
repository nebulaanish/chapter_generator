import { useState } from "react";

interface Props {
  formData: { url: string };
  setFormData: React.Dispatch<React.SetStateAction<any>>;
}

export default function URLInput({ formData, setFormData }: Props) {
  const [error, setError] = useState<string>("");

  const validateURL = (url: string): boolean => {
    const pattern = new RegExp(
      "^(https?:\\/\\/)?" + // protocol
        '((([a-zA-Z0-9$-_@.&+!*"(),]|[a-zA-Z0-9-])+(:[0-9]+)?)|(([0-9]{1,3}\\.){3}[0-9]{1,3}))' +
        '(\\/[a-zA-Z0-9$-_@.&+!*"(),]*)*$',
      "i"
    );
    return pattern.test(url);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    if (validateURL(value)) {
      setError("");
      setFormData({ ...formData, url: value });
    } else {
      setError("Invalid URL");
    }
  };

  return (
    <div>
      <label className="block text-sm font-medium mb-2">Enter URL</label>
      <input
        type="text"
        value={formData.url}
        onChange={handleChange}
        placeholder="https://example.com"
        className="block w-full text-sm border-gray-300 rounded-md py-2 px-1.5"
      />
      {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
    </div>
  );
}
