import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from openai import OpenAI

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("Please set OPENAI_API_KEY in a .env file")

client = OpenAI()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """
    Expects JSON like:
    {
      "messages": [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."},
        ...
      ]
    }
    """
    data = request.get_json(force=True)
    messages = data.get("messages", [])

    try:
        resp = client.chat.completions.create(
            model="gpt-5-nano",
            messages=messages,
            temperature=1,
        )
        content = resp.choices[0].message.content
        return jsonify({"reply": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health") # debugging
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(debug=True)
