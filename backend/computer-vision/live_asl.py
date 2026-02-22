from typing import Any


from ultralytics import YOLO
import cv2
from collections import Counter

# We are using the YOLO11L model; To set model, put in path to model file inside YOLO()
model = YOLO("yolo11l.pt")

# cap is variable for using cv2.VideoCapture(0) where 0 is normally the webcam of your computer.
# link to documentation used: https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html
cap = cv2.VideoCapture(0)

# Exclude these letters because signing them is super hard and my hand is tired.
# Make sure these are capitizled. 
EXCLUDED_NAMES = {"J", "Z", "T", "C", "G", "A"} 

# list allowed_indices is a list of the class IDs of the letters that are allowed; 
allowed_indices = []
    
# for loop inside checks all possible class names from model, excluding letters from EXCLUDED_NAMES
for class_id, class_name in model.names.items():
    if class_name not in EXCLUDED_NAMES:
        allowed_indices.append(class_id)

# last_output keeps track of the last output letter, so we don't avoid duplicate letters
# This is to accommodate the fact that the model processses faster than we can sign since we're new.
last_output = None

# While the webcam is working, do:
while cap.isOpened():

    frames = []
# We collect # of frames to aggregate and average the results of predictions from YOLOv11.
    for _ in range(11):
# Two outputs from cap.read():
# success: True if frame is read correctly, else False
# frame: The frame read from the webcam in (I think) BGR format
        success, frame = cap.read()
# if even single frame collection fails, break the loop
        if not success:
            break
        frames.append(frame)
# from list frames, if length < 11, break while capisOpened() loop
# TLDR; Shutsdown webcam
    if len(frames) < 11:
        break

# ultralytics inference documentation = https://docs.ultralytics.com/usage/cfg/#predict-settings 
# conf is confidence threshold
# iou is intersection-over-union threshold; how much overlap between bounding boxes is allowed
# verbose = False to suppress unnecessary output
# classes = Only use allowed classes from allowed_indices list
    results = model(frames, conf=0.25, iou=0.45, verbose=False, classes=allowed_indices)

# Initialize counter for frames with detections
    frames_with_detections = 0
# all_classes = list of aggregated classes detected
    all_classes = []
# for each result in results, get the class of the predicted bounding box
    for r in results:
# frame_classes = list of classes detected in the current result; box.cls will be an id so convert to int
# we do r.boxes because the model allows multiple bounding boxes/classes per frame; Althought our case is ually just one
        frame_classes = [model.names[int(box.cls[0])] for box in r.boxes]
# basically if frame_classes is not empty, continue
        if frame_classes:
            frames_with_detections += 1
# Note to self: use .extend instead of .append since frame_classes is also a list
            all_classes.extend(frame_classes)

    batch_size = len(results)

# avoids ties and ensures we can do majority vote
# ensure at least more than half the frames have a class detected
    if all_classes and (frames_with_detections > (batch_size // 2)):
# from python import collections, Counter counts # of times element appears in list & returns first tuple, first element of that tuple
        most_common = Counter[Any](all_classes).most_common(1)[0][0]
# if this does not equal last output, print to terminal and set last_output to this new class/letter
        if most_common != last_output:
            print(most_common)
            last_output = most_common

# Note to self: remember to relesae webcam
cap.release()