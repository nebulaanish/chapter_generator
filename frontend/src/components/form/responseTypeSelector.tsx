interface Props {
  formData: { responseType: string };
  setFormData: React.Dispatch<React.SetStateAction<any>>;
}

export default function ResponseTypeSelector({ formData, setFormData }: Props) {
  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setFormData({ ...formData, responseType: e.target.value });
  };

  return (
    <div>
      <label className="block text-sm font-medium mb-2"> Response Type </label>
      <select
        value={formData.responseType}
        onChange={handleChange}
        className="block w-full text-sm border-gray-300 rounded-md py-2 px-1.5"
      >
        <option value="profession"> Profession </option>
        <option value="technical"> Technical </option>
      </select>
    </div>
  );
}
