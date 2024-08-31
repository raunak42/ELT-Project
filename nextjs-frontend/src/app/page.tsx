import FileUpload from "./components/FileUpload";

export default async function Home() {
  const res = await fetch("http://0.0.0.0:8000/hello", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ user_name: "Faramir" }),
    cache:"no-store"
  });
  const data = await res.json();
  console.log(data);

  return (
    <div>
      <FileUpload />
    </div>
  );
}
