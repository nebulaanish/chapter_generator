interface Props {
  formData: { file: File | null };
  setFormData: React.Dispatch<React.SetStateAction<any>>;
}

export default function FileUpload({ formData, setFormData }: Props) {
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      console.log(e.target.files);
      setFormData({ ...formData, file: e.target.files[0] });
    }
  };

  return (
    <div>
      <label className="block text-sm font-medium mb-2"> File Upload</label>
      <input
        type="file"
        onChange={handleFileChange}
        className="block w-full text-sm border-gray-300 rounded-md"
      />
    </div>
  );
}
