"use client";

import React, { useEffect, useRef, useState } from "react";
import Image from "next/image";

interface VideoLLMProps {
  setTranscript: React.Dispatch<React.SetStateAction<string[]>>;
}

export default function VideoLLM({ setTranscript }: VideoLLMProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const isCapturingRef = useRef(true);
  const [status, setStatus] = useState("Initializing camera...");
  const [lastScreenshot, setLastScreenshot] = useState<string | null>(null);

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
        startCapturing();
      } catch (error) {
        console.error("Camera error:", error);
        setStatus("Camera access denied");
      }
    };

    initCamera();

    return () => {
      isCapturingRef.current = false;

      if (streamRef.current) {
        streamRef.current.getTracks().forEach((track) => track.stop());
      }
    };
  }, []);

  const captureAndSend = (): Promise<void> => {
    return new Promise((resolve, reject) => {
      if (!videoRef.current || !canvasRef.current) {
        resolve();
        return;
      }

      const video = videoRef.current;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    if (!ctx) {
      resolve();
      return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Update preview
    const imageBase64 = canvas.toDataURL("image/jpeg");
    setLastScreenshot(imageBase64);

    // Send as real file
    canvas.toBlob(async (blob) => {
      if (!blob) {
        resolve();
        return;
      }

      const formData = new FormData();
      formData.append("file", blob, "screenshot.jpg");

      try {
        const response = await fetch("http://127.0.0.1:8000/interpret", {
          method: "POST",
          body: formData,
        });

        const data = await response.json();
        //console.log("Backend response:", data);

        if (data.letter) {
          setTranscript((prev) => [...prev, data.letter]);
        }
        resolve();
      } catch (error) {
        console.error("Upload error:", error);
        reject(error);
      }
    }, "image/jpeg");
  });
};

  const startCapturing = async () => {
    const run = async () => {
      while (isCapturingRef.current) {
        await captureAndSend();
        await new Promise((r) => setTimeout(r, 0));
      }
    };
    run();
  };

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

      {lastScreenshot && (
        <Image
          src={lastScreenshot}
          alt="Last Screenshot"
          width={256}
          height={256}
          className="w-64 rounded shadow"
        />
      )}

      <canvas ref={canvasRef} className="hidden" />
    </div>
  );
}
