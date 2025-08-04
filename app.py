import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS  # ✅ ADD THIS
import os
import anthropic

app = Flask(__name__)
CORS(app)  # ✅ ENABLE CORS FOR ALL ROUTES

def get_anthropic_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")

    print("🔍 Runtime API Key:", api_key[:10] + "..." if api_key else "❌ None found")

    if not api_key:
        raise ValueError("❌ Anthropic API key not found in environment variables.")
    
    return anthropic.Anthropic(api_key=api_key)

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
        client = get_anthropic_client()
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=200,
            messages=[{"role": "user", "content": user_prompt}]
        )

        # Log response structure for debugging
        print("🔁 Claude API raw response:", response)

        # Get message text safely
        content_list = response.content
        if content_list and isinstance(content_list, list):
            return jsonify({"response": content_list[0].text})
        else:
            return jsonify({"error": "Invalid response format from Claude"}), 500

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

