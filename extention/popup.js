const api = "http://127.0.0.1:5000";

document.getElementById("startBtn").onclick = () => {
  fetch(api + "/start", { method: "POST" });
};

document.getElementById("stopBtn").onclick = () => {
  fetch(api + "/stop", { method: "POST" });
};

document.getElementById("summaryBtn").onclick = () => {
  fetch(api + "/summary", { method: "POST" })
    .then(res => res.json())
    .then(data => {
      const link = document.createElement("a");
      link.href = "http://127.0.0.1:5000/static/hasil/hasil_meeting.pdf";
      link.download = "hasil_meeting.pdf";
      link.click();
    });
};
