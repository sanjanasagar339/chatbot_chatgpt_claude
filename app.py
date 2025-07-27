from flask import Flask, request, jsonify
from anthropic import Anthropic  # ✅ Anthropic SDK
import os
from dotenv import load_dotenv
from flask_cors import CORS

# Load .env variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Claude (Anthropic) client
client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

greetings = ["hi", "hello", "hey", "hola", "howdy", "greetings", "sup", "yo"]

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_prompt = data.get("prompt", "").strip().lower()

    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400

    if user_prompt in greetings:
        return jsonify({"response": "Hello! How can I assist you today?"})

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",  # Or another Claude model like claude-3-sonnet-20240229
            max_tokens=1000,
            temperature=0.7,
            messages=[
                {"role": "user", "content": user_prompt}
            ]
        )
        reply = response.content[0].text
        return jsonify({"response": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
