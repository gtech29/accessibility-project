from elevenlabs.client import ElevenLabs
from elevenlabs import save
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('API_KEY')

VOICE_ID = "21m00Tcm4TlvDq8ikWAM"

client = ElevenLabs(api_key=API_KEY)


def get_voice_settings(emotion):

    emotion = emotion.lower()

    if emotion == "happy":
        print("Detected emotion: HAPPY")
        return {
            "stability": 0.2,
            "similarity_boost": 0.9,
            "style": 0.9,
            "use_speaker_boost": True
        }

    elif emotion == "sad":
        print("Detected emotion: SAD")
        return {
            "stability": 0.7,
            "similarity_boost": 0.9,
            "style": 0.3,
            "use_speaker_boost": True
        }

    elif emotion == "angry":
        print("Detected emotion: ANGRY")
        return {
            "stability": 0.3,
            "similarity_boost": 0.85,
            "style": 1.0,
            "use_speaker_boost": True
        }

    elif emotion == "excited":
        print("Detected emotion: EXCITED")
        return {
            "stability": 0.15,
            "similarity_boost": 0.9,
            "style": 1.0,
            "use_speaker_boost": True
        }

    elif emotion == "neutral":
        print("Detected emotion: NEUTRAL")
        return {
            "stability": 0.5,
            "similarity_boost": 0.9,
            "style": 0.5,
            "use_speaker_boost": True
        }

    else:
        print("Emotion not recognized, using NEUTRAL")
        return {
            "stability": 0.35,
            "similarity_boost": 0.9,
            "style": 0.85,
            "use_speaker_boost": True
        }


def speak(text, emotion):

    voice_settings = get_voice_settings(emotion)

    print(f"Text: {text}")
    print(f"Emotion received from LLM: {emotion}")

    audio = client.text_to_speech.convert(
        text=text,
        voice_id=VOICE_ID,
        model_id="eleven_multilingual_v2",
        voice_settings=voice_settings
    )

    filename = f"output_{emotion}.mp3"

    
    save(audio, filename)

    full_path = os.path.abspath(filename)

    print("Saved to:", full_path)

    
    


if __name__ == "__main__":

    llm_outputs = [
        {"text": "Hi, it's so good to see you!", "emotion": "happy"},
        {"text": "I miss you...", "emotion": "sad"},
        {"text": "Okay, everything is fine.", "emotion": "neutral"},
        {"text": "This is unbelievable!", "emotion": "excited"},
    ]

    for output in llm_outputs:
        speak(output["text"], output["emotion"])