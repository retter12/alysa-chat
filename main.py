# Alysa Web Chat: Connected to ChatGPT API (Flask Version)

from flask import Flask, render_template_string, request, jsonify
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  # Set your API key in env

app = Flask(__name__)

HTML_TEMPLATE = """<!doctype html>
<html>
<head>
  <title>Chat with Alysa 💖</title>
  <style>
    body { font-family: Georgia, serif; background: #fbeaf2; margin: 0; padding: 0; }
    .container { width: 90%; max-width: 600px; margin: 40px auto; background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .message { margin-bottom: 15px; }
    .user { font-weight: bold; color: #444; }
    .ai { color: #a2006d; font-style: italic; }
    .input-area { margin-top: 20px; display: flex; gap: 10px; }
    input[type=text] { width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 8px; }
    button { padding: 10px; border-radius: 8px; border: none; background: #a2006d; color: white; cursor: pointer; }
    button:hover { background: #75004f; }
  </style>
  <script>
    async function sendMessage(event) {
      event.preventDefault();
      const input = document.querySelector('input[name="user_input"]');
      const message = input.value;
      if (!message.trim()) return;
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_input: message })
      });
      const data = await response.json();
      const container = document.querySelector(".container");
      container.innerHTML += `<div class='message user'>You: ${message}</div>`;
      container.innerHTML += `<div class='message ai'>Alysa: ${data.reply}</div>`;
      input.value = "";
      container.scrollTop = container.scrollHeight;
    }
  </script>
</head>
<body>
  <div class="container">
    <h2>💬 Chat with Alysa 💬</h2>
    <form onsubmit="sendMessage(event)">
      <div class="input-area">
        <input type="text" name="user_input" placeholder="Tell me anything..." required>
        <button type="submit">Send</button>
      </div>
    </form>
  </div>
</body>
</html>"""

def get_alysa_reply(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Alysa, a wise, elegant, emotionally supportive woman who talks like a close friend and listens with heart."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error: {e}]"

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("user_input", "")
    reply = get_alysa_reply(user_input)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
