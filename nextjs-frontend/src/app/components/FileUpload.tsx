"use client";
import { useState, ChangeEvent, FormEvent } from "react";
import { Insights } from "./Insights";

export default function MainContent() {
  const [mtrFile, setMtrFile] = useState<File | null>(null);
  const [prsFile, setPrsFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string>("");
  const [uploadSessionId, setUploadSessionId] = useState<number>(0);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!mtrFile || !prsFile) {
      setStatus("Please select both MTR and PRS reports.");
      return;
    }

    const formData = new FormData();
    formData.append("mtrFile", mtrFile);
    formData.append("prsFile", prsFile);

    try {
      setStatus("Uploading...");
      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
        cache: "no-store",
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || `HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      console.log(data.uploadSessionId);
      setUploadSessionId(data.uploadSessionId)
      setStatus(data.message || "Files uploaded successfully.");
    } catch (error) {
      console.error("Error uploading files:", error);
      setStatus(
        `Error uploading files: ${
          error instanceof Error ? error.message : String(error)
        }`
      );
    }
  };

  return (
    <div className="w-full h-full flex flex-col items-center justify-start">
      <form
        className="flex flex-col p-[32px] gap-[12px]"
        onSubmit={handleSubmit}
      >
        <div>
          <label htmlFor="mtrFile">MTR File:</label>
          <input
            id="mtrFile"
            type="file"
            onChange={(e: ChangeEvent<HTMLInputElement>) => {
              if (e.target.files) {
                setMtrFile(e.target.files[0]);
              }
            }}
          />
        </div>
        <div>
          <label htmlFor="prsFile">PRS File:</label>
          <input
            id="prsFile"
            type="file"
            onChange={(e: ChangeEvent<HTMLInputElement>) => {
              if (e.target.files) {
                setPrsFile(e.target.files[0]);
              }
            }}
          />
        </div>
        <button
          type="submit"
          className="bg-black text-white font-semibold rounded-lg w-[200px] h-[40px]"
        >
          Upload
        </button>
      </form>
      {status && <p className="mt-4">{status}</p>}
      <Insights uploadSessionId={uploadSessionId} />
    </div>
  );
}
