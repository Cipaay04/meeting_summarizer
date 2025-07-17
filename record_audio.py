# record_audio.py
import pyaudio
import wave
import threading

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 600  # 10 menit

frames = []
audio_interface = pyaudio.PyAudio()
stream = None
recording = False


def start_recording():
    global stream, frames, recording
    recording = True
    frames = []
    stream = audio_interface.open(format=FORMAT, channels=CHANNELS,
                                   rate=RATE, input=True,
                                   frames_per_buffer=CHUNK)
    print("🎙️ Merekam audio...")

    def record_loop():
        while recording:
            try:
                data = stream.read(CHUNK)
                frames.append(data)
            except Exception as e:
                print("⚠️ Error saat merekam:", e)
                break

    threading.Thread(target=record_loop, daemon=True).start()


def stop_recording():
    global recording
    recording = False
    stream.stop_stream()
    stream.close()
    audio_interface.terminate()

    with wave.open("audio.wav", 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio_interface.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    print("✅ Rekaman selesai dan disimpan sebagai audio.wav")
