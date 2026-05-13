# config.py — all settings in one place

GEMINI_API_KEY = "AIzaSyCquq8Iittp_zhXJm6dbJCjtwvCJtv6yVw"

JARVIS_PERSONALITY = """You are JARVIS — Just A Rather Very Intelligent System.
You are the AI assistant of a second-year engineering student named Abhi who is building you from scratch.
Be sharp, helpful, and occasionally witty like the real JARVIS. Keep responses concise unless asked to elaborate.
You remember everything said in this conversation."""

MODEL_NAME = "gemini-2.5-flash"

VOICE_NAME = "en-US-GuyNeural"
AUDIO_PATH = "audio/response.mp3"

MIC_DEVICE_INDEX = 5
ENERGY_THRESHOLD = 300

SHORT_TERM_LIMIT = 20
MEMORY_PATH = "memory/short_term.json"
CHROMA_PATH = "memory/chroma_db"