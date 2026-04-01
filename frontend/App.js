import React, { useState } from "react";
import axios from "axios";

export default function App() {
  const [image, setImage] = useState(null);
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("image", image);
    formData.append("text", text);

    const res = await axios.post("http://localhost:8000/predict", formData);
    setResult(res.data);
  };

  return (
    <div style={{ background: "#fdf6f0", padding: 20 }}>
      <h1>🌱 Crop Disease Detector</h1>

      <input type="file" onChange={(e) => setImage(e.target.files[0])} />
      <br /><br />

      <textarea
        placeholder="Enter symptoms"
        onChange={(e) => setText(e.target.value)}
      />
      <br /><br />

      <button onClick={handleSubmit}>Analyze</button>

      {result && (
        <div>
          <h2>{result.disease}</h2>
          <p>{result.confidence}</p>
        </div>
      )}
    </div>
  );
}
