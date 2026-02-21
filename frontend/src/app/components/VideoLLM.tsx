"use client";

import { useEffect, useRef, useState } from "react";

interface VideoLLMProps {
  setTranscript: React.Dispatch<React.SetStateAction<string[]>>;
}

export default function VideoLLM({ setTranscript }: VideoLLMProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const isRunningRef = useRef<boolean>(false);

  const [status, setStatus] = useState("Initializing camera...");

  useEffect(() => {
    const initCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: "user" },
          audio: false,
        });

        streamRef.current = stream;

        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }

        setStatus("Camera active");
      } catch (error) {
        console.error("Camera error:", error);
        setStatus("Camera access denied");
      }
    };

    const waitForVideoReady = () =>
      new Promise<void>((resolve) => {
        if (!videoRef.current) return resolve();

        if (videoRef.current.readyState >= 2) {
          resolve();
        } else {
          videoRef.current.onloadedmetadata = () => resolve();
        }
      });

    const processFrame = async () => {
      if (!videoRef.current || !canvasRef.current) return;

      const video = videoRef.current;
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      if (!ctx) return;

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);

      // This is where YOLO inference would happen
      // const detection = await runYolo(imageData);
      // const llmResponse = await sendToBackend(detection);

      // Simulated async inference delay (~5fps)
      await new Promise((resolve) => setTimeout(resolve, 200));

      // Simulate receiving a full interpreted sentence occasionally
      if (Math.random() > 0.985) {
        const simulatedSentence = "Simulated interpreted sentence.";

        setTranscript((prev) => [...prev, simulatedSentence]);
      }
    };

    const startLoop = async () => {
      isRunningRef.current = true;

      await waitForVideoReady();

      while (isRunningRef.current) {
        await processFrame();
      }
    };

    const start = async () => {
      await initCamera();
      await startLoop();
    };

    start();

    return () => {
      isRunningRef.current = false;

      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, [setTranscript]);

  return (
    <div className="flex flex-col items-center gap-4">
      <h1 className="text-2xl font-semibold">{status}</h1>

      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        className="w-full max-w-2xl rounded-lg shadow-lg bg-black"
      />

      <canvas ref={canvasRef} className="hidden" />
    </div>
  );
}
