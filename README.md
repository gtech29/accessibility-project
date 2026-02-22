# Group 6 | Accessibility Project

## What It Does

This project is an **AI-powered American Sign Language (ASL) translator** that converts sign language gestures into natural, conversational text and speech in real time. It addresses a common challenge for deaf and hard of hearing individuals: word-for-word translation tools often produce awkward or out-of-context output. This system instead:

1. **Captures** video from your webcam
2. **Detects** ASL hand signs using computer vision (YOLO)
3. **Translates** letter sequences into coherent, grammatically correct sentences using a large language model (Gemma)
4. **Displays** the result as natural text and inferred emotion

The frontend streams frames to the backend, which runs YOLO for sign detection and Ollama & Gemma for language refinement.

---

## Technologies Used

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI, CORSMiddleware |
| **Computer Vision** | YOLO11L (Ultralytics) |
| **LLM** | Gemma 3 via Ollama |
| **Frontend** | Next.js, React, Tailwind CSS |

---

## Setup

### Prerequisites

- **Python 3.12.7**
- **Node.js 18+** and **npm**
- **Ollama** (for running **Gemma** locally)
- **Webcam** (for sign language input)
- **Audio Output Device** (i.e speakers)

### 1. Install Ollama and Gemma

[Download and install Ollama](https://ollama.ai), then pull the Gemma model:

In the terminal or Git Bash, do:
```bash
ollama pull gemma3
```

### 2. Backend Setup

In the terminal or Git Bash, do:
```bash
cd backend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install fastapi uvicorn numpy opencv-python ultralytics ollama
```

Start the backend server:

In the terminal or Git Bash, do:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at `http://127.0.0.1:8000`. The first request may take a few seconds while the camera/YOLO model initializes.

### 3. Frontend Setup

In a separate terminal or Git Bash:

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:3000`.

### 4. Run the App

1. Ensure **Ollama** is running (`ollama serve` or the Ollama app)
2. Start the **backend** (port 8000)
3. Start the **frontend** (port 3000)
4. Open `http://localhost:3000` in your browser
5. Allow camera access and sign in front of the webcam

---

## Project Structure

```
accessibility-project/
├── backend/
│   ├── main.py              # FastAPI app, /interpret endpoint
│   ├── computer_vision/
│   │   ├── live_asl.py      # YOLO ASL detection & frame buffering
│   │   └── yolo11l.pt       # YOLO11L model weights
│   └── llm/
│       └── llm_processing.py # Gemma-based sentence & emotion refinement
├── frontend/
│   └── src/
│       └── app/
│           ├── page.tsx     # Main page layout
│           └── components/
│               ├── VideoLLM.tsx   # Webcam capture & API calls
│               └── TextToScreen.tsx # Transcript display
└── README.md
```

---

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/interpret` | POST | Accepts an image file (multipart/form-data). Returns detected sign sequence refined into a sentence and emotion. |

---

## Notes

- The YOLO model recognizes ASL letters; some letters (J, Z, T, C, G, A) are excluded by default due to signing difficulty.
- Frames are buffered and processed in batches to improve detection stability.
- The LLM expands common abbreviations (e.g., "hbu" → "how about you") and infers emotion from the text.
- Originally CORSMiddleware was to be used for cross-domain
