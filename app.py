import traceback
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import anthropic

load_dotenv()

app = Flask(__name__)
api_key = os.getenv("ANTHROPIC_API_KEY")
print("Loaded API Key:", api_key[:8] + "..." if api_key else "❌ None found")
client = anthropic.Anthropic(api_key=api_key)

@app.route("/")
def home():
    return "Claude Chatbot is running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_prompt = data.get("prompt", "")

    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return jsonify({"response": response.content[0].text})
    except Exception as e:
        traceback.print_exc() 
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
