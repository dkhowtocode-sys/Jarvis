# jarvis.py — entry point

from voice import speak, listen
from brain import get_response, detect_topic, summarize_and_store
from memory import load_short_term

def main():
    history = load_short_term()

    print("=" * 50)
    print("  J.A.R.V.I.S. — Online")
    print("  Type 'exit' to shut down")
    print("=" * 50 + "\n")

    speak("J.A.R.V.I.S. online. Good to see you, Abhi.")

    message_count = 0

    while True:
        user_input = listen()

        if not user_input:
            continue

        if user_input.lower() == "exit":
            # summarize and store before shutting down
            topic = detect_topic(history)
            summarize_and_store(history, topic)
            speak("Shutting down. Good day, Abhi.")
            break

        reply, history = get_response(user_input, history)
        speak(reply)

        message_count += 1

        # every 10 messages, detect topic and store to long term memory
        if message_count % 10 == 0:
            topic = detect_topic(history)
            summarize_and_store(history, topic)

main()