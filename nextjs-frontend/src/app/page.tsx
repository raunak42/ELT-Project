import { BASE_URL } from "@/lib/constants";
import MainContent from "./components/FileUpload";

export default async function Home() {
  const res = await fetch(`${BASE_URL}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    cache: "no-store",
  });
  const data = await res.json();
  console.log(data);

  return (
    <div className="py-[48px]" >
      <MainContent />
    </div>
  );
}
