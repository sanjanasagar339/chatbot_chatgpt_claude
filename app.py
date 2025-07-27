# app.py

from flask import Flask, request, jsonify
from anthropic import Anthropic
import os

app = Flask(__name__)

# Get Claude API key from environment
CLAUDE_KEY = os.getenv("CLAUDE_API_KEY")

# Debug print to confirm key is set (optional – remove in production)
print("Claude API Key:", "Set ✅" if CLAUDE_KEY else "❌ Not Found")

# Initialize the Claude client
client = Anthropic(api_key=CLAUDE_KEY)

@app.route("/", methods=["GET"])
def home():
    return "Claude API Flask server is running."

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")

        if not prompt:
            return jsonify({"error": "No prompt provided"}), 400

        response = client.messages.create(
            model="claude-3-sonnet-20240229",  # You can change this to claude-3-opus or claude-3-haiku if needed
            max_tokens=1000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return jsonify({"reply": response.content[0].text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
