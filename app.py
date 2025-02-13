from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import os
import whisper
import json

app = Flask(__name__)
CORS(app)

# OpenAI API key (store in .env for security)
OPENAI_API_KEY = "your_openai_api_key_here"
openai.api_key = OPENAI_API_KEY

# Initialize Whisper model
model = whisper.load_model("base")

UPLOAD_FOLDER = "uploads"
DATA_FILE = "data.json"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# 🟢 Route: Render UI
@app.route("/")
def index():
    return render_template("index.html")


# 🟢 Route: Upload & Transcribe Podcast
@app.route("/upload", methods=["POST"])
def upload_podcast():
    if "podcast" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["podcast"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Transcribe using Whisper
    transcription = model.transcribe(filepath)
    transcript_text = transcription["text"]

    # Generate Summary using GPT
    prompt = f"Summarize this podcast: {transcript_text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=200
    )
    summary = response["choices"][0]["message"]["content"]

    # Store in JSON file
    podcast_data = {"title": file.filename, "transcript": transcript_text, "summary": summary}
    save_data(podcast_data)

    return jsonify({"title": file.filename, "summary": summary})


# 🟢 Route: Search Summaries
@app.route("/search", methods=["GET"])
def search_podcasts():
    query = request.args.get("query", "").lower()
    data = load_data()

    results = [entry for entry in data if query in entry["summary"].lower()]
    return jsonify(results)


# 📝 Save Data to JSON File
def save_data(new_entry):
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(new_entry)

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


# 📂 Load Data from JSON File
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


if __name__ == "__main__":
    app.run(debug=True)
