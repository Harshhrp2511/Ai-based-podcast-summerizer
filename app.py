from flask import Flask, request, jsonify, render_template
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Ensure OpenAI API key is set
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY. Check your .env file.")

# Initialize OpenAI client correctly for v1.0.0+
client = openai.OpenAI(api_key=OPENAI_API_KEY)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_podcast():
    if "podcast" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["podcast"]
    title = file.filename

    # Dummy summary generation
    summary = generate_summary(f"Transcript of {title}")

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
    """Generate a summary using OpenAI API (Updated for API v1.0.0+)"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Summarize this podcast: {text}"}]
        )
        return response.choices[0].message.content.strip()  # Ensure clean output
    except Exception as e:
        return f"Error generating summary: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
