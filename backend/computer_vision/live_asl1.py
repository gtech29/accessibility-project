import streamlit as st
import cv2
from collections import Counter
from ultralytics import YOLO

st.set_page_config(page_title="ASL Fingerspelling", layout="wide")
st.title("ASL Live Inference")

model = YOLO("yolo11l.pt")
EXCLUDED_NAMES = {"J", "Z", "T", "C", "G", "K", "Y", "A", "O"}
allowed_indices = [i for i, name in model.names.items() if name not in EXCLUDED_NAMES]

# Sidebar
BATCH_SIZE = st.sidebar.slider("Batch size", 2, 10, 5)
conf = st.sidebar.slider("Confidence", 0.0, 1.0, 0.25)
st.sidebar.markdown("---")
st.sidebar.markdown("**Output appears in:**")
st.sidebar.markdown("- Terminal (console)")
st.sidebar.markdown("- Below the video")
st.sidebar.markdown("**To stop:** Press `Ctrl+C` in the terminal or close the browser tab.")

if st.sidebar.button("Start", key="start_btn"):
    cap = cv2.VideoCapture(0)
    last_output = None

    frame_placeholder = st.empty()
    output_container = st.empty()

    while cap.isOpened():
        frames = []
        for _ in range(BATCH_SIZE):
            success, frame = cap.read()
            if not success:
                break
            frames.append(frame)

        if len(frames) < BATCH_SIZE:
            break

        results = model(frames, conf=conf, iou=0.45, verbose=False, classes=allowed_indices)

        frames_with_detections = 0
        all_classes = []
        for r in results:
            frame_classes = [model.names[int(box.cls[0])] for box in r.boxes]
            if frame_classes:
                frames_with_detections += 1
                all_classes.extend(frame_classes)

        batch_size = len(results)
        if all_classes and frames_with_detections > batch_size // 2:
            most_common = Counter(all_classes).most_common(1)[0][0]
            if most_common != last_output:
                print(most_common)  # Goes to terminal
                last_output = most_common
                output_container.markdown(f"### Last letter: **{most_common}**")

        # Display self-view video only
        frame_placeholder.image(frames[0], channels="BGR")

    cap.release()