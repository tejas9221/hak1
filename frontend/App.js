import React, { useState } from "react";
import axios from "axios";
import { Bar } from "react-chartjs-2";

export default function App() {
  const [image, setImage] = useState(null);
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);

  // 🎤 Voice input
  const startVoice = () => {
    const recognition = new window.webkitSpeechRecognition();
    recognition.onresult = (event) => {
      setText(event.results[0][0].transcript);
    };
    recognition.start();
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("image", image);
    formData.append("text", text);

    const res = await axios.post(
      "https://your-backend-url.onrender.com/predict",
      formData
    );

    setResult(res.data);
  };

  return (
    <div style={{ background: "#fdf6f0", padding: 20 }}>
      <h1 style={{ color: "#7a9e9f" }}>🌱 AI Crop Detector</h1>

      <input type="file" onChange={(e) => setImage(e.target.files[0])} />
      <br /><br />

      <textarea
        placeholder="Enter symptoms..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <br /><br />

      <button onClick={startVoice}>🎤 Voice</button>
      <button onClick={handleSubmit}>Analyze</button>

      {result && (
        <div>
          <h2>Disease: {result.disease}</h2>
          <p>Confidence: {result.confidence}</p>

          <Bar
            data={{
              labels: ["Healthy", "Leaf Spot", "Rust", "Blight"],
              datasets: [
                {
                  label: "Prediction",
                  data: result.graph,
                },
              ],
            }}
          />

          <p>💡 Tips: {result.tips}</p>
        </div>
      )}
    </div>
  );
}
