import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { fetchMeetingById } from "../api/meetings";
import "../MeetingDetails.css";

export default function MeetingDetails() {
  const { id } = useParams();
  const [meeting, setMeeting] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let intervalId;

    const loadMeeting = async () => {
      try {
        const data = await fetchMeetingById(id);
        setMeeting(data);

        // If not yet processed, set interval to poll every 3s
        if (data.status !== "processed") {
          intervalId = setInterval(async () => {
            const updated = await fetchMeetingById(id);
            setMeeting(updated);
            if (updated.status === "processed") {
              clearInterval(intervalId); // Stop polling when done
            }
          }, 3000);
        }
      } catch (err) {
        setError("Failed to load meeting details");
      }
    };

    loadMeeting();

    return () => clearInterval(intervalId); // Cleanup
  }, [id]);

  if (error) return <div className="error-message">{error}</div>;
  if (!meeting) return <div className="loading-message">Loading...</div>;

  return (
    <div className="meeting-details-container">
      {/* Background Blobs */}
      <div className="background-blobs">
        <div className="blob blob-1"></div>
        <div className="blob blob-2"></div>
        <div className="blob blob-3"></div>
      </div>

      {/* Main Content */}
      <div className="content-container">
        <h2 className="meeting-title">{meeting.title}</h2>

        <div className="content-box">
          <h3 className="section-title">
            <span>📄</span> Transcription
          </h3>
          <div className="content-box-inner">
            <p className="section-content">
              {meeting.status === "processed"
                ? meeting.transcript
                : "Processing...It may take few Mins"}
            </p>
          </div>
        </div>

        <div className="content-box">
          <h3 className="section-title">
            <span>🧠</span> Summary
          </h3>
          <div className="content-box-inner">
            <p className="section-content">
              {meeting.status === "processed"
                ? meeting.summary
                : "Processing...It may take few Mins"}
            </p>
          </div>
        </div>

        <div className="content-box">
          <h3 className="section-title">
            <span>😊</span> Emotions
          </h3>
          <div className="content-box-inner">
            <p className="section-content">
              {meeting.status === "processed"
                ? meeting.emotion
                : "Processing...It may take few Mins"}
            </p>
          </div>
        </div>

        <div className="content-box">
          <h3 className="section-title">
            <span>✅</span> Action Items
          </h3>
          <div className="content-box-inner">
            <p className="section-content">
              {meeting.status === "processed"
                ? meeting.action_items
                : "Processing...It may take few Mins"}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
