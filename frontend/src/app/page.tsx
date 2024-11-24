import CourseOutlineForm from "@/components/courseOutlineForm";

export default function Home() {
  return (
    <div className="w-full ">
      <h1 className="text-2xl font-bold text-center mb-8 mt-6">
        AI Powered Chapter Generator
      </h1>
      <CourseOutlineForm />
    </div>
  );
}
