let mediaRecorder;
let audioChunks = [];

document.getElementById("startBtn").onclick = async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);

  mediaRecorder.ondataavailable = (e) => {
    audioChunks.push(e.data);
  };

  mediaRecorder.onstop = async () => {
    const blob = new Blob(audioChunks, { type: "audio/wav" });
    const formData = new FormData();
    formData.append("audio", blob, "audio.wav");

    await fetch("http://localhost:5000/transcribe", {
      method: "POST",
      body: formData,
    });

    await fetch("http://localhost:5000/summary", {
      method: "POST",
    });

    // Download hasil ringkasan
    const link = document.createElement("a");
    link.href = "http://localhost:5000/static/hasil/ringkasan.txt";
    link.download = "ringkasan.txt";
    link.click();
  };

  mediaRecorder.start();
  console.log("🎙️ Rekaman dimulai...");
};

document.getElementById("stopBtn").onclick = () => {
  mediaRecorder.stop();
  console.log("⏹️ Rekaman dihentikan.");
};
