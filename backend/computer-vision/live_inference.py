from ultralytics import solutions

# pip install ultralytics
# pip install lap
# To test, run streamlit run live_inference.py

# Code from https://docs.ultralytics.com/guides/streamlit-live-inference/#streamlit-application-code

inf = solutions.Inference(
    model="yolo11l.pt",  # open-source model by https://huggingface.co/atalaydenknalbant
)
inf.inference()
