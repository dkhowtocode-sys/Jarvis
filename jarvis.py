import speech_recognition as sr
import edge_tts
import asyncio
import os
from google import genai
from google.genai import types

recognizer = sr.Recognizer()

def speak (text):
    print(f"\nJARVIS: {text}\n")
    async def _speak():
        communicate = edge_tts.Communicate(text, voice="en-US-GuyNeural")
        await communicate.save("response.mp3")
    asyncio.run(_speak())
    os.system("mpg123 -q response.mp3")

def listen():
    with sr.Microphone(device_index=5) as source:
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = False
        print("listening...")
           
        try: 
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=8) 
            text = recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text
        except sr.UnknownValueError:
            speak("i didn't catch that, could you repeat?")
            return ""
        except sr.WaitTimeoutError:
            return ""


JARVIS_PERSONALITY = """You are JARVIS — Just A Rather Very Intelligent System. 
You are the AI assistant of a second-year engineering student named Abhi who is building you from scratch.
Be sharp, helpful, and occasionally witty like the real JARVIS. Keep responses concise unless asked to elaborate.
You remember everything said in this conversation."""

client=genai.Client(api_key="AIzaSyCquq8Iittp_zhXJm6dbJCjtwvCJtv6yVw")
chat = client.chats.create(model="gemini-2.5-flash")

conversation_history = []
print ('=' * 50)
print("J.A.R.V.I.S - online")
print(" Type 'exit' to shut down")
print("-"* 50 + "\n")

speak("J.A.R.V.I.S. online. Good to see you, Abhi.")

while True:
    user_input = listen()

    if not user_input:
        continue
    if user_input.lower() == "exit":
        speak("shutting down, good day, abhi.")
        break

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    response = chat.send_message(
        user_input,
        config=types.GenerateContentConfig(
            system_instruction=JARVIS_PERSONALITY
        )
        )
    
    reply = response.text
    speak(reply)
    
    conversation_history.append({
        "role":"assistant",
        "content": reply
    })

    print(f"\nJARVIS: {reply}\n")