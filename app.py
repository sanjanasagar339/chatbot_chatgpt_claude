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
        
        instruction = (
            "Please answer all user questions concisely. "
            "Use 1-2 line definitions or 3-5 sentence summaries. "
            "Avoid long paragraphs unless the user explicitly asks for details."
        )
        
        lower_prompt = user_prompt.lower()
        if "define" in lower_prompt or "what is" in lower_prompt:
            instruction = "Give a very short 1-2 line definition only."
        elif "brief" in lower_prompt:
            instruction = "Give a brief explanation in 3-5 lines only."
        elif "list" in lower_prompt or "key factors" in lower_prompt or "points" in lower_prompt:
            instruction = "List the points clearly, keep it short."

        final_prompt = f"{instruction}\n\nUser: {user_prompt}"

        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=250,
            temperature=0.3,
            messages=[
                {"role": "user", "content": final_prompt}
            ]
        )

        content_list = response.content
        if content_list and isinstance(content_list, list):
            return jsonify({"response": content_list[0].text.strip()})
        else:
            return jsonify({"error": "Invalid response format from Claude"}), 500

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
        
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
