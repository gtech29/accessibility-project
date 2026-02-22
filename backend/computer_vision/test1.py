from ultralytics import YOLO
import cv2

model = YOLO("yolo11l.pt")
cap = cv2.VideoCapture(0)  # or path to video file

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Run inference - results is the model output
    results = model(frame, conf=0.25, iou=0.45)

    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        cls_name = model.names[cls_id]
        conf = float(box.conf[0])
        xyxy = box.xyxy[0].tolist()
        print(f"Class {cls_name}")

cap.release()