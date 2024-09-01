import MainContent from "./components/FileUpload";

export default async function Home() {
  const res = await fetch("http://0.0.0.0:8000", {
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
