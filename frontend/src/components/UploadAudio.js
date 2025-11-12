import React, { useState } from "react";
import axios from "axios";

const UploadAudio = () => {
    const [file,setFile] = useState(null);
    const [result,setResult] = useState(null);
    const [loading,setLoading] = useState(null);
    const [error,setError] = useState(null);

    const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000"; // ✅ use env var if available

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
        setResult(null);
        setError(" ");
    };

    const handleUpload = async () =>{
        if(!file){
            setError("Please select a file first!");
            return;
        }
        const formData = new FormData();
        formData.append("file",file);

        try{
            setLoading(true);
            const response = await axios.post(
                `${API_URL}/predict`, // ✅ dynamically use backend URL
                formData,
                { headers: { "Content-Type": "multipart/form-data" } }
            );
            setResult(response.data);
        }catch(err){
            setError("Prediction failed. Check backend logs.");
        }finally{
            setLoading(false);
        }
    };

    return (
    <div className="upload-box">
      <input type="file" accept=".au" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Processing..." : "Predict Genre"}
      </button>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="result-box">
          <h3>🎶 Prediction Result</h3>
          <p><strong>Genre:</strong> {result.predicted_class}</p>
          <p><strong>Confidence:</strong> {result.confidence}</p>
        </div>
      )}
    </div>
  );
}

export default UploadAudio;