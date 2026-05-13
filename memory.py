# memory.py — short term and long term memory for JARVIS

import json
import os
import chromadb
from datetime import datetime
from config import MEMORY_PATH, CHROMA_PATH, SHORT_TERM_LIMIT

# ── SHORT TERM ──
def load_short_term():
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r") as f:
            return json.load(f)
    return []

def save_short_term(history):
    # keep only last SHORT_TERM_LIMIT messages
    trimmed = history[-SHORT_TERM_LIMIT:]
    with open(MEMORY_PATH, "w") as f:
        json.dump(trimmed, f, indent=2)

def add_to_short_term(history, role, content):
    history.append({"role": role, "content": content})
    save_short_term(history)
    return history

# ── LONG TERM (ChromaDB) ──
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = chroma_client.get_or_create_collection(name="jarvis_memory")

def save_long_term(topic, content):
    doc_id = f"{topic}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    collection.add(
        documents=[content],
        metadatas=[{"topic": topic, "timestamp": str(datetime.now())}],
        ids=[doc_id]
    )
    print(f"[Memory] Saved to long term: {topic}")

def search_long_term(query, n_results=3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    if results and results["documents"]:
        return results["documents"][0]
    return []

def get_memory_context(query):
    memories = search_long_term(query)
    if not memories:
        return ""
    context = "\n".join(memories)
    return f"\n[JARVIS Memory — relevant context]:\n{context}\n"