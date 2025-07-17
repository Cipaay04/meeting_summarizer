# app.py
from flask import Flask, request, jsonify, send_from_directory
import os
import whisper
import threading

from record_audio import start_recording, stop_recording
from summarize import generate_summary

app = Flask(__name__)

recording_thread = None

@app.route("/")
def index():
    return "🚀 API Meeting Summarizer aktif!"

# -----------------------------
# ✅ Endpoint: Mulai rekaman
# -----------------------------
@app.route("/start", methods=["POST"])
def start():
    global recording_thread
    recording_thread = threading.Thread(target=start_recording)
    recording_thread.start()
    return "🎙️ Perekaman dimulai"

# -----------------------------
# ✅ Endpoint: Hentikan rekaman
# -----------------------------
@app.route("/stop", methods=["POST"])
def stop():
    stop_recording()
    return "🛑 Perekaman dihentikan dan disimpan"

# -----------------------------
# ✅ Endpoint: Transkripsi
# -----------------------------
@app.route("/transcribe", methods=["POST"])
def transcribe():
    audio_path = "static/hasil/audio.wav"
    if not os.path.exists(audio_path):
        return jsonify({"error": "❌ File audio.wav tidak ditemukan di static/hasil/"}), 400

    print("🔍 Menjalankan Whisper (small) untuk transkripsi...")
    model = whisper.load_model("small")
    result = model.transcribe(audio_path, language="indonesian")
    transcript = result["text"]

    os.makedirs("static/hasil", exist_ok=True)
    with open("static/hasil/transkrip.txt", "w", encoding="utf-8") as f:
        f.write(transcript)

    return jsonify({"transkrip": transcript})

# -----------------------------
# ✅ Endpoint: Ringkasan
# -----------------------------
@app.route("/summary", methods=["POST"])
def summary():
    try:
        summary_text = generate_summary()
        return jsonify({"summary": summary_text})
    except FileNotFoundError as fnf:
        return jsonify({"error": str(fnf)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -----------------------------
# ✅ Endpoint: Download file hasil
# -----------------------------
@app.route('/static/hasil/<path:filename>')
def download_file(filename):
    return send_from_directory('static/hasil', filename)

# -----------------------------
# ✅ Menjalankan server
# -----------------------------
if __name__ == "__main__":
    print("📡 Menjalankan server Flask di http://127.0.0.1:5000")
    app.run(debug=True)
