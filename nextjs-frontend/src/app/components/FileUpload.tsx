"use client";
import { useState, ChangeEvent, FormEvent } from "react";
import { Insights } from "./Insights";
import Image from "next/image";

export default function MainContent() {
  const [mtrFile, setMtrFile] = useState<File | null>(null);
  const [prsFile, setPrsFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string>("");
  const [uploadSessionId, setUploadSessionId] = useState<number>(0);
  const [showSpinner, setShowSpinner] = useState<boolean>(false);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setShowSpinner(true);
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
      setShowSpinner(false);
      setUploadSessionId(data.uploadSessionId);
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
    <div className="w-full h-full flex flex-col items-center justify-start gap-[12px]">
      <form
        className="flex flex-col p-[32px] gap-[32px]  items-center justify-start border rounded-lg h-[360px]"
        onSubmit={handleSubmit}
      >
        <h1 className="text-2xl font-semibold" >Select files</h1>
        <div>
          <label
            htmlFor="mtrFile"
            className="block text-sm font-medium text-[#000000] mb-2"
          >
            MTR File
          </label>
          <input
            id="mtrFile"
            type="file"
            onChange={(e: ChangeEvent<HTMLInputElement>) => {
              if (e.target.files) {
                setMtrFile(e.target.files[0]);
              }
            }}
            className="w-full text-sm text-[#000000]
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-zinc-100 file:text-[#000000]
                hover:file:bg-zinc-200
              "
          />
        </div>
        <div>
          <label
            htmlFor="prsFile"
            className="block text-sm font-medium text-[#000000] mb-2"
          >
            Payment Sheet
          </label>
          <input
            id="prsFile"
            type="file"
            onChange={(e: ChangeEvent<HTMLInputElement>) => {
              if (e.target.files) {
                setPrsFile(e.target.files[0]);
              }
            }}
            className="w-full text-sm text-[#000000]
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-zinc-100 file:text-[#000000]
                hover:file:bg-zinc-200
              "
          />
        </div>
        <button
          type="submit"
          className={`bg-black text-white font-semibold rounded-lg w-[200px] h-[40px] disabled:cursor-not-allowed disabled:bg-zinc-400 flex items-center justify-center`}

        >
          {!showSpinner ? (
            <h1>Upload</h1>
          ) : (
            <Image
              alt=""
              width={24}
              height={24}
              src={"/spinner.svg"}
              className="animate-spin"
            />
          )}
        </button>
      </form>
      {<p className="mt-4 h-[30px]">{status}</p>}
      <Insights uploadSessionId={uploadSessionId} />
    </div>
  );
}
