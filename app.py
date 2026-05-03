import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import anthropic

app = Flask(__name__)
CORS(app)

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
    try:
        data = request.get_json(force=True)   # ✅ FIX
        print("📥 Incoming data:", data)

        user_prompt = data.get("prompt") if data else None
        instruction = ("Answer the question directly. "
        "Do NOT repeat the question. "
        "Do NOT use headings, markdown, or special formatting. "
        "Give a simple, clean, short answer.")
        final_prompt = instruction + "\n\n" + user_prompt

        if not user_prompt:
            return jsonify({"error": "No prompt provided"}), 400

        client = get_anthropic_client()

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{"role": "user", "content": user_prompt}]
        )

        raw_text = response.content[0].text
        clean_text = raw_text.replace("\n", " ") \
                     .replace("#", "") \
                     .replace("*", "") \
                     .replace("•", "") \
                     .strip()
        clean_text = " ".join(clean_text.split())

        return jsonify({"response": clean_text})
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
