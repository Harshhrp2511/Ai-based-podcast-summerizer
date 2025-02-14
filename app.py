from flask import Flask, request, jsonify, render_template
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import os

app = Flask(__name__)

# Load Gemma 2B Model
MODEL_NAME = "google/gemma-2b"
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading {MODEL_NAME} on {device}...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).to(device)
print("Model loaded successfully!")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_podcast():
    if "podcast" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["podcast"]
    title = file.filename

    # Dummy transcript (replace with real transcription logic)
    transcript = f"This is the transcript of {title}"

    # Generate summary using Gemma 2B
    summary = generate_summary(transcript)

    return jsonify({"title": title, "summary": summary})

@app.route("/search", methods=["GET"])
def search_podcast():
    query = request.args.get("query", "")

    # Dummy data
    results = [
        {"title": "Podcast 1", "summary": "This is a summary."},
        {"title": "Podcast 2", "summary": "Another summary."},
    ]

    filtered_results = [r for r in results if query.lower() in r["title"].lower()]
    return jsonify(filtered_results)

def generate_summary(text):
    """Generate a summary using Gemma 2B"""
    try:
        input_text = f"Summarize this podcast transcript: {text}"
        inputs = tokenizer(input_text, return_tensors="pt").to(device)

        with torch.no_grad():
            outputs = model.generate(**inputs, max_length=100)

        summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return summary
    except Exception as e:
        return f"Error generating summary: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
