# brain.py — Gemini API calls and conversation logic

from google import genai
from google.genai import types
from config import GEMINI_API_KEY, JARVIS_PERSONALITY, MODEL_NAME
from memory import (
    load_short_term,
    add_to_short_term,
    get_memory_context,
    save_long_term
)

client = genai.Client(api_key="AIzaSyCquq8Iittp_zhXJm6dbJCjtwvCJtv6yVw")

def get_response(user_input, history):
    # search long term memory for relevant context
    memory_context = get_memory_context(user_input)

    # build system prompt with memory injected
    system = JARVIS_PERSONALITY
    if memory_context:
        system += memory_context

    # add user message to history
    history = add_to_short_term(history, "user", user_input)

    # send to Gemini
    response = client.chats.create(model=MODEL_NAME).send_message(
        user_input,
        config=types.GenerateContentConfig(
            system_instruction=system
        )
    )

    reply = response.text

    # add JARVIS reply to history
    history = add_to_short_term(history, "assistant", reply)

    return reply, history

def detect_topic(history):
    if len(history) < 4:
        return "general"

    last_messages = history[-6:]
    convo = "\n".join([f"{m['role']}: {m['content']}" for m in last_messages])

    response = client.chats.create(model=MODEL_NAME).send_message(
        f"""Read this conversation and reply with ONE word — the topic being discussed.
Examples: music, university, project, weather, food, coding
Conversation:
{convo}
Topic:"""
    )
    topic = response.text.strip().lower().split()[0]
    return topic

def summarize_and_store(history, topic):
    if len(history) < 4:
        return

    convo = "\n".join([f"{m['role']}: {m['content']}" for m in history[-10:]])

    response = client.chats.create(model=MODEL_NAME).send_message(
        f"""Summarize the key facts from this conversation in 3-5 bullet points.
Be concise. Only include facts worth remembering long term about the user.
Conversation:
{convo}
Summary:"""
    )

    summary = response.text.strip()
    save_long_term(topic, summary)