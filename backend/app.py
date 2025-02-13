from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import whisper
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB setup
client = MongoClient(os.getenv("MONGO_URI"))
db = client["podcast_db"]
collection = db["summaries"]

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Whisper model
model = whisper.load_model("base")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


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
    prompt = f"Summarize this podcast in a short, concise way: {transcript_text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=200
    )
    summary = response["choices"][0]["message"]["content"]

    # Store in MongoDB
    podcast_data = {
        "title": file.filename,
        "transcript": transcript_text,
        "summary": summary
    }
    collection.insert_one(podcast_data)

    return jsonify({"title": file.filename, "summary": summary})


# 🔍 Route: Search Summaries
@app.route("/search", methods=["GET"])
def search_podcasts():
    query = request.args.get("query", "").lower()
    results = collection.find({"summary": {"$regex": query, "$options": "i"}})

    podcasts = [{"title": r["title"], "summary": r["summary"]} for r in results]
    return jsonify(podcasts)


if __name__ == "__main__":
    app.run(debug=True)
