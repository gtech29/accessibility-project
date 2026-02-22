"use client";

import { useState } from "react";
import VideoLLM from "./components/VideoLLM";
import TextToScreen from "./components/TextToScreen";

export default function Home() {
  const [transcript, setTranscript] = useState<string[]>([]);

  return (
    <main className="min-h-screen flex flex-col md:flex-row p-40 gap-4">
      <div className="w-full md:w-1/2">
        <VideoLLM setTranscript={setTranscript} />
      </div>

      <div className="w-full md:w-1/2">
        <TextToScreen transcript={transcript} />
      </div>
    </main>
  );
}
