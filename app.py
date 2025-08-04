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

        # Modify the user input to suggest behavior based on its content
        if "define" in user_prompt.lower() or "what is" in user_prompt.lower():
            instruction = "Please give a very concise answer, ideally 1-2 lines only."
        elif "brief" in user_prompt.lower():
            instruction = "Please give a short but complete explanation, around 3-5 lines."
        else:
            instruction = "Respond clearly and naturally."

        full_prompt = f"{instruction}\n\n{user_prompt}"

        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,  # allow enough room for full sentences
            messages=[{"role": "user", "content": full_prompt}]
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



