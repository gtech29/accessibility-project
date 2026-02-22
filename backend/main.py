from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
from computer_vision.live_asl import process_frame

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/interpret")
async def interpret(file: UploadFile = File(...)):
    contents = await file.read()
    if not contents:
        return {"error": "No file uploaded"}

    np_array = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if image is None:
        return {"error": "Could not decode image"}

    # Run YOLO
    letter = process_frame(image)

    return {"letter": letter}