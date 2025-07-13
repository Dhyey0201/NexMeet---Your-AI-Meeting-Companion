import { useState } from "react";

export default function MeetingForm() {
  const [inputType, setInputType] = useState("file");
  const [title, setTitle] = useState("");
  const [file, setFile] = useState(null);
  const [fileUrl, setFileUrl] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!title) {
      alert("Please enter meeting title");
      return;
    }

    if (inputType === "file" && !file) {
      alert("Please select a file");
      return;
    }

    if (inputType === "url" && !fileUrl) {
      alert("Please enter a file URL");
      return;
    }

    const formData = new FormData();
    formData.append("title", title);

    if (inputType === "file") {
      formData.append("file", file);
    } else {
      formData.append("file_url", fileUrl);
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/meetings", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const error = await response.json();
        alert("Error: " + error.detail);
        return;
      }

      const data = await response.json();
      alert("Upload successful: " + JSON.stringify(data));
      // Optionally reset form
      setTitle("");
      setFile(null);
      setFileUrl("");
    } catch (err) {
      alert("Network error: " + err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 400, margin: "auto" }}>
      <h2>Create New Meeting</h2>

      <label>
        Title:
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
      </label>

      <div>
        <label>
          <input
            type="radio"
            value="file"
            checked={inputType === "file"}
            onChange={() => setInputType("file")}
          />
          Upload File
        </label>
        <label style={{ marginLeft: 20 }}>
          <input
            type="radio"
            value="url"
            checked={inputType === "url"}
            onChange={() => setInputType("url")}
          />
          Enter URL
        </label>
      </div>

      {inputType === "file" ? (
        <input
          type="file"
          accept="audio/*,video/*"
          onChange={(e) => setFile(e.target.files[0])}
          required
        />
      ) : (
        <input
          type="url"
          placeholder="https://example.com/audio.mp4"
          value={fileUrl}
          onChange={(e) => setFileUrl(e.target.value)}
          required
        />
      )}

      <button type="submit" style={{ marginTop: 20 }}>
        Submit
      </button>
    </form>
  );
}
