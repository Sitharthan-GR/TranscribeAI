import React, { useState } from "react";
import axios from 'axios';


const VideoToSummary = () => {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<
    "initial" | "uploading" | "success" | "fail"
  >("initial");
  const [summary, setSummaryResult]=useState<string>("");
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setStatus("initial");
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (file) {
      setStatus("uploading");

      const formData = new FormData();
      formData.append("video", file);

      try {
        const response = await axios.post('http://127.0.0.1:5000/summarize_video', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        
        console.log(response);
        setStatus("success");
        setSummaryResult(response.data.summary);
      } catch (error) {
        console.error(error);
        setStatus("fail");
      }
    }
  };

  return (
    <>
      <div className="input-group">
        <label htmlFor="file" className="sr-only">
          Choose a file
        </label>
        <input id="file" type="file" onChange={handleFileChange} />
      </div>
      {file && (
        <section>
          File details:
          <ul>
            <li>Name: {file.name}</li>
            <li>Type: {file.type}</li>
            <li>Size: {file.size} bytes</li>
          </ul>
        </section>
      )}

      {file && (
        <button onClick={handleUpload} className="submit">
          Upload a file
        </button>
      )}

      <Result status={status} />

      <Summary summary={summary} />
    </>
  );
};

const Result = ({ status }: { status: string }) => {
  if (status === "success") {
    return <p>✅ Summarized the video successfully!</p>;
  } else if (status === "fail") {
    return <p>❌ File upload failed!</p>;
  } else if (status === "uploading") {
    return <p>⏳ Summarizing the video...</p>;
  } else {
    return null;
  }
};

const Summary = ({summary}:{summary: string}) =>{

  if (summary !== ""){
    return <p className="summary-text"> <b>Summary:</b> {summary}</p>
  }
}

export default VideoToSummary;