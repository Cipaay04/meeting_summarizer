# summarize.py
from transformers import pipeline
import os

def generate_summary():
    summarizer = pipeline("summarization", model="cahya/bart-large")

    transkrip_path = "static/hasil/transkrip.txt"
    if not os.path.exists(transkrip_path):
        raise FileNotFoundError("❌ transkrip.txt tidak ditemukan")

    with open(transkrip_path, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    hasil = []

    for chunk in chunks:
        summary = summarizer(chunk, max_length=250, min_length=80, do_sample=False)[0]["summary_text"]
        hasil.append(summary)

    final = "\n\n".join(hasil)

    with open("static/hasil/ringkasan.txt", "w", encoding="utf-8") as f:
        f.write(final)

    return final
