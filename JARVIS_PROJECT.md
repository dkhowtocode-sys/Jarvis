# J.A.R.V.I.S — Project Documentation
> Just A Rather Very Intelligent System  
> Built by Abhi — 2nd Year Engineering Student  
> Inspired by Iron Man. Built from scratch.

---

## Project Overview

JARVIS is a personal AI assistant built entirely from scratch over a series of phases. The goal is to replicate the experience of Tony Stark's JARVIS — a voice-driven, context-aware, action-capable AI that knows you personally and can control your environment.

This is not a tutorial project. Every line of code is written by hand with full understanding of what it does.

---

## Project Structure

```
jarvis/
├── jarvis.py          ← entry point
├── brain.py           ← Gemini API + conversation logic
├── voice.py           ← listen() and speak()
├── memory.py          ← short term + ChromaDB long term
├── config.py          ← all settings and constants
├── server.py          ← Flask bridge (UI ↔ brain)
├── jarvis_ui.html     ← frontend (Canvas orb UI)
│
├── memory/
│   ├── short_term.json
│   └── chroma_db/
│
├── audio/
│   └── response.mp3
│
└── venv/
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| AI Brain | Google Gemini 2.5 Flash (via `google-genai`) |
| Voice Input | SpeechRecognition + PyAudio |
| Voice Output | edge-tts + mpg123 |
| UI | HTML + CSS + Canvas API |
| Backend | Flask + flask-cors |
| Memory (Short Term) | JSON file (rolling window) |
| Memory (Long Term) | ChromaDB (vector database) |
| OS | Ubuntu 24 (live USB boot) |
| Editor | VS Code |

---

## How To Run

```bash
# Terminal 1 — start the Flask server
cd ~/jarvis
source venv/bin/activate
python3 server.py

# Terminal 2 — open the UI
firefox jarvis_ui.html

# OR run terminal-only JARVIS
python3 jarvis.py
```

---

## Phases

### ✅ Phase 1 — Core Brain
**Status: Complete**

The foundation. A Python script with a conversation loop that sends messages to Gemini and maintains a session history list so JARVIS remembers context within a session.

Key concepts learned:
- How LLM APIs work (messages array, system prompt, tokens)
- Conversation history as memory — every message appended to a list and sent in full each time
- System prompts as personality injection

**Libraries:** `google-genai`

---

### ✅ Phase 2 — Voice
**Status: Complete**

JARVIS can hear and talk back.

**Hearing:** `SpeechRecognition` + PyAudio captures mic, converts to text via Google Speech API. Device index 5 (PulseAudio) for Ubuntu compatibility.

**Speaking:** `edge-tts` with `en-US-GuyNeural` voice. Audio saved to `audio/response.mp3` and played via `mpg123`.

Key concepts learned:
- `asyncio` for async TTS generation
- PulseAudio vs ALSA audio routing on Linux
- PyAudio compilation dependencies

**Libraries:** `SpeechRecognition`, `pyaudio`, `edge-tts`

---

### ✅ Phase 2.5 — UI/UX
**Status: Complete**

Standalone HTML/CSS/Canvas interface. Dark minimal aesthetic.

**Design:**
- Deep navy background (`#02030b`) with radial blue atmospheric glow
- Central energy orb — 4 orbital rings with non-uniform luminance
- Each ring segment drawn in 5 passes: wide bloom → medium glow → sharp bright → white-hot core → pure white peak
- Orb reacts to state: idle → listening → thinking → speaking
- Equaliser: 28 bars in bell curve shape, random heights at ~80ms intervals, appears only during listening
- Conversation feed below orb with animated message entry
- Type mode toggle for text input fallback

**File:** `jarvis_ui.html`

---

### ✅ Phase 3 — Memory
**Status: Complete**

Two-layer memory system.

#### Short Term Memory
- Rolling window of last 20 messages per session
- Saved to `memory/short_term.json` — survives restarts
- Loaded automatically on every boot

#### Long Term Memory (RAG)
- **ChromaDB** local vector database at `memory/chroma_db/`
- Embedding model: `all-MiniLM-L6-v2` (auto downloaded by ChromaDB)
- Every 10 messages: topic detector AI labels the conversation
- On exit: summarizer AI compresses thread into key facts → stored in ChromaDB
- On each new message: user input → vector → ChromaDB similarity search → relevant memories injected into Gemini context

#### The Three AI Calls
```
1. JARVIS          — main conversation (Gemini)
2. Topic Detector  — labels conversation topic (Gemini)
3. Summarizer      — compresses thread to key facts (Gemini)
```

#### Memory Pipeline
```
You speak
    ↓
Short term — rolling 20 msgs saved to JSON
    ↓
Every 10 msgs — topic detector runs
    ↓
On exit — summarizer compresses + stores to ChromaDB
    ↓
Next session — relevant memories retrieved + injected
    ↓
JARVIS responds like he never forgot
```

**Libraries:** `chromadb`

---

### ✅ Phase 4 Start — Flask Bridge
**Status: In Progress**

Flask server connects the UI to the JARVIS brain over HTTP.

```
Browser (jarvis_ui.html)
    ↓ POST /chat
Flask (server.py)
    ↓
brain.py → Gemini → memory
    ↓
Reply returned to browser
    ↓
UI displays + edge-tts speaks
```

**Endpoints:**
- `POST /chat` — send message, get reply
- `GET /status` — check if server is online

**Libraries:** `flask`, `flask-cors`

---

### 📋 Phase 4 — Agentic AI (Planned)
**Status: Planned**

JARVIS stops just talking and starts doing things.

Planned tools:
- Open apps (Spotify, browser, terminal)
- Web search with real results
- Read/write files on disk
- Camera vision (OpenCV + Gemini Vision)
- Set reminders

**Camera Vision:** OpenCV captures frame → base64 encoded → sent to Gemini alongside message → JARVIS can see and describe what the camera sees.

**Auto Launch on Startup:** systemd service that starts JARVIS automatically when Ubuntu boots. No terminal needed.

---

### 📋 Beyond Phase 4 — The Ecosystem (Vision)

- Always-on wake word detection ("Hey JARVIS")
- Custom desktop window (Electron or PyQt)
- IoT integration — smart lights, sensors
- Local AI models (no internet required)
- Mobile companion app

---

## Architecture Overview

```
┌─────────────────────────────────────┐
│           jarvis_ui.html            │  ← Face
└─────────────────┬───────────────────┘
                  │ HTTP POST /chat
┌─────────────────▼───────────────────┐
│              server.py              │  ← Flask bridge
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│              brain.py               │  ← Gemini API
├─────────────────────────────────────┤
│            memory.py                │
│   ├── short_term.json               │  ← Session history
│   └── chroma_db/                    │  ← Vector store
├─────────────────────────────────────┤
│             voice.py                │
│   ├── listen() — SpeechRecognition  │  ← Ears
│   └── speak()  — edge-tts           │  ← Mouth
└─────────────────────────────────────┘
```

---

## Key Concepts Learned

| Concept | Where Used |
|---|---|
| LLM API calls | Phase 1 |
| System prompts | Phase 1 |
| Conversation history as memory | Phase 1 |
| Async Python (asyncio) | Phase 2 |
| Audio I/O on Linux | Phase 2 |
| Canvas 2D rendering + glow effects | Phase 2.5 |
| RAG (Retrieval Augmented Generation) | Phase 3 |
| Vector embeddings | Phase 3 |
| Separation of concerns (modular code) | Phase 3 refactor |
| REST APIs (Flask) | Phase 4 |
| Agentic tool use | Phase 4 (upcoming) |

---

## Setup Commands (Fresh Start)

```bash
# 1. Clone repo
git clone https://github.com/dkhowtocode-sys/Jarvis.git
cd jarvis

# 2. Create environment
python3 -m venv venv
source venv/bin/activate

# 3. Install libraries
pip install google-genai
pip install SpeechRecognition pyaudio edge-tts
pip install chromadb
pip install flask flask-cors

# 4. System dependencies
sudo apt install portaudio19-dev python3-dev gcc mpg123 pulseaudio -y

# 5. Add your API key to config.py

# 6. Run
python3 server.py       # start Flask
firefox jarvis_ui.html  # open UI
```

---

## Notes

- API: Google Gemini 2.5 Flash (free tier via AI Studio)
- Live USB Ubuntu — remember to push to GitHub, nothing persists on reboot
- Every new terminal: `cd ~/jarvis && source venv/bin/activate`
- `.gitignore` excludes `venv/`, `chroma_db/`, `response.mp3`, `__pycache__/`

---

*"The truth is… I am Iron Man."*
*— and you're building his brain.*
