# summarize.py
from transformers import pipeline
import os

def generate_summary():
    print("🔄 Memuat model cahya/bart-large...")
    try:
        summarizer = pipeline("summarization", model="cahya/bart-large")
    except Exception as e:
        print("❌ Gagal memuat model:", e)
        raise e

    if not os.path.exists("static/hasil/transkrip.txt"):
        raise FileNotFoundError("File transkrip.txt tidak ditemukan di folder static/hasil/")

    with open("static/hasil/transkrip.txt", "r", encoding="utf-8") as f:
        full_text = f.read()

    print("🧠 Memproses ringkasan...")
    chunk_size = 1000
    chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]

    summaries = []
    for idx, chunk in enumerate(chunks):
        try:
            print(f"   ⏳ Ringkasan bagian {idx+1}/{len(chunks)}...")
            summary = summarizer(chunk, max_length=250, min_length=80, do_sample=False)[0]["summary_text"]
            summaries.append(summary)
        except Exception as e:
            print(f"⚠️ Gagal merangkum bagian {idx+1}: {e}")

    final_summary = "\n\n".join(summaries)

    with open("static/hasil/ringkasan.txt", "w", encoding="utf-8") as f:
        f.write(final_summary)

    print("✅ Ringkasan disimpan ke static/hasil/ringkasan.txt")
    return final_summary
