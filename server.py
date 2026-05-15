# server.py — Flask bridge between UI and JARVIS brain

from flask import Flask, request, jsonify
from flask_cors import CORS
from brain import get_response
from voice import speak
from memory import load_short_term

app = Flask(__name__)
CORS(app)

history = load_short_term()

@app.route('/chat', methods=['POST'])
def chat():
    global history
    data = request.json
    user_input = data.get('message', '')
    if not user_input:
        return jsonify({'reply': ''})
    reply, history = get_response(user_input, history)
    speak(reply)
    return jsonify({'reply': reply})

@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'online'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)