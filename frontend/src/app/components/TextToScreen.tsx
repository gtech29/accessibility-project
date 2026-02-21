"use client";

interface TextToScreenProps {
  transcript: string[];
}

export default function TextToScreen({ transcript }: TextToScreenProps) {
  return (
    <main className="min-h-screen bg-zinc-50 dark:bg-black p-6 overflow-y-auto">
      <div className="max-w-3xl mx-auto space-y-4">
        <h1 className="text-3xl font-bold text-center">Interpreted Text</h1>

        {transcript.length === 0 ? (
          <p className="text-gray-500 dark:text-gray-400 text-center">
            Waiting for interpretation...
          </p>
        ) : (
          transcript.map((sentence, index) => (
            <div
              key={index}
              className="p-4 rounded-xl bg-white dark:bg-zinc-800 shadow"
            >
              <p className="text-lg leading-relaxed">{sentence}</p>
            </div>
          ))
        )}

      </div>
    </main>
  );
}
