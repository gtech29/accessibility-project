from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
from computer_vision.live_asl import process_frame
from llm.llm_processing import process_llm
from elevenlab.elevenlabs1 import process_elevenlabs
import asyncio

camera_ready = False

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
    global camera_ready

    if not camera_ready:
        print("Initializing camera... Please wait 5 seconds")
        await asyncio.sleep(5)
        camera_ready = True

    contents = await file.read()
    if not contents:
        return {"error": "No file uploaded"}

    np_array = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if image is None:
        return {"error": "Could not decode image"}

    # Run YOLO
    yolo_result_string = process_frame(image)

    if yolo_result_string is None:
        return {"Error": "No sign detected"}
    
    llm_results_dict = process_llm(yolo_result_string)
    #llm_results_dict = {"Sentence":"I love you", "Emotion": "happy"}


    mp3_filepath = process_elevenlabs(llm_results_dict)

    print(mp3_filepath)

    #return {"word": llm_results_dict}
    return {"word": mp3_filepath}