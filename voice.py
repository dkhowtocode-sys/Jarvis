# voice.py — ears and mouth of JARVIS

import speech_recognition as sr
import edge_tts
import asyncio
import os
from config import VOICE_NAME, AUDIO_PATH, MIC_DEVICE_INDEX, ENERGY_THRESHOLD

recognizer = sr.Recognizer()

def speak(text):
    print(f"\nJARVIS: {text}\n")
    async def _speak():
        communicate = edge_tts.Communicate(text, voice=VOICE_NAME)
        await communicate.save(AUDIO_PATH)
    asyncio.run(_speak())
    os.system(f"mpg123 -q {AUDIO_PATH}")

def listen():
    with sr.Microphone(device_index=MIC_DEVICE_INDEX) as source:
        recognizer.energy_threshold = ENERGY_THRESHOLD
        recognizer.dynamic_energy_threshold = False
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)
            text = recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text
        except sr.UnknownValueError:
            speak("I didn't catch that. Could you repeat?")
            return ""
        except sr.WaitTimeoutError:
            return ""