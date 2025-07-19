# app.py
from flask import Flask, request, jsonify
import whisper
from summarize import generate_summary
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static/hasil"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return "✅ Meeting Summarizer API aktif di Render!"

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "audio" not in request.files:
        return jsonify({"error": "❌ File audio tidak ditemukan"}), 400

    audio_file = request.files["audio"]
    path = os.path.join(UPLOAD_FOLDER, "audio.wav")
    audio_file.save(path)

    model = whisper.load_model("medium")
    result = model.transcribe(path, language="indonesian")

    with open(os.path.join(UPLOAD_FOLDER, "transkrip.txt"), "w", encoding="utf-8") as f:
        f.write(result["text"])

    return jsonify({"transkrip": result["text"]})

@app.route("/summary", methods=["POST"])
def summary():
    try:
        result = generate_summary()
        return jsonify({"summary": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
