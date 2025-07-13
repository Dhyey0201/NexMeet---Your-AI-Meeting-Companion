"""from celery_worker import celery_app
from services.transcriber import transcribe_audio
from db.models import meetings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from services.summarizer import summarize_text
from services.emotion_detector import predict_emotion
import requests
import os
import re
import uuid

# Setup sync DB engine
DATABASE_URL = "postgresql+psycopg2://dhyeypatel:Dhyey%402003@localhost/meetings_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


import requests
import re

def convert_gdrive_url_to_direct(url: str) -> str:
    match = re.search(r'/d/([^/]+)', url)
    if match:
        file_id = match.group(1)
        return f'https://drive.google.com/uc?export=download&id={file_id}'
    return url

def download_file_from_url(url: str, local_path: str) -> str:
    # Convert Google Drive URL to direct download if applicable
    url = convert_gdrive_url_to_direct(url)

    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raises if status != 200

    content_type = response.headers.get('Content-Type', '')
    if 'text/html' in content_type:
        raise RuntimeError("URL returned an HTML page, not a file. Check the URL or file permissions.")

    with open(local_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    # Optional: check file size to ensure file is not empty or too small
    import os
    file_size = os.path.getsize(local_path)
    if file_size < 1000:  # adjust threshold as needed
        raise RuntimeError("Downloaded file size too small, likely invalid file.")

    return local_path


# Helper function to download audio from a given URL
def download_audio_from_url(url: str, save_path: str):
    response = requests.get(url)
    response.raise_for_status()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, 'wb') as f:
        f.write(response.content)

@celery_app.task
def transcribe_meeting_task(meeting_id: str, file_url: str):
    session = SessionLocal()
    local_file_path = f"/tmp/{meeting_id}.mp4"  # or .mp3 depending on the file type
    
    try:
        print(f"Started transcription for meeting {meeting_id} with URL {file_url}")

        # Step 1: Mark as processing
        session.execute(
            meetings.update().where(meetings.c.id == meeting_id).values(status="processing")
        )
        session.commit()

        # Step 2: Download file locally
        download_file_from_url(file_url, local_file_path)

        # Step 3: Transcribe using local file path
        transcript = transcribe_audio(local_file_path)
        print(f"Transcription result: {transcript[:200]}")

        # Step 4: Emotion detection
        emotion = predict_emotion(local_file_path)
        print(f"Detected emotion: {emotion}")

        # Step 5: Summarize transcript
        summary = summarize_text(transcript)

        # Step 6: Save transcript, summary, emotion in DB and mark transcribed
        session.execute(
            meetings.update().where(meetings.c.id == meeting_id).values(
                status="transcribed",
                transcript=transcript,
                summary=summary,
                emotion=emotion
            )
        )
        session.commit()
        print("Transcript, summary, and emotion saved successfully.")

    except SQLAlchemyError as e:
        session.rollback()
        print("DB error occurred:", e)
        session.execute(
            meetings.update().where(meetings.c.id == meeting_id).values(
                status="failed", transcript=str(e)
            )
        )
        session.commit()
        raise e

    except Exception as e:
        session.rollback()
        print("General error:", e)
        session.execute(
            meetings.update().where(meetings.c.id == meeting_id).values(
                status="failed", transcript=str(e)
            )
        )
        session.commit()
        raise e

    finally:
        # Clean up the downloaded file if exists
        if os.path.exists(local_file_path):
            os.remove(local_file_path)
        session.close()


import os
from services.transcriber import transcribe_audio
from ai_model.inference import extract_action_items  # 👈 import this
from db.models import meetings
from db.database import database
from celery_worker import celery_app
import requests
import uuid

def download_file_from_url(url: str, local_path: str) -> str:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(local_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return local_path

@celery_app.task(name="tasks.transcription_task.transcribe_meeting_task")
def transcribe_meeting_task(meeting_id: str, file_url: str):
    try:
        print(f"Started transcription for meeting {meeting_id} with URL {file_url}")

        # Step 1: Download video/audio
        local_file_path = f"/tmp/{meeting_id}.mp4"
        download_file_from_url(file_url, local_file_path)

        # Step 2: Transcribe the audio
        transcript = transcribe_audio(local_file_path)

        # Step 3: Extract action items from transcript
        action_items = extract_action_items(transcript)
        action_text = "; ".join(action_items)

        # Step 4: Update DB with results
        query = meetings.update().where(meetings.c.id == meeting_id).values(
            status="completed",
            transcript=transcript,
            action_items=action_text
        )
        database.execute(query)

        print("Transcription & action item extraction completed!")

        os.remove(local_file_path)

    except Exception as e:
        print("General error:\n", e)
        query = meetings.update().where(meetings.c.id == meeting_id).values(
            status="failed",
            transcript=str(e)
        )
        database.execute(query)
"""

import os
import re
import requests
from services.transcriber import transcribe_audio
from services.summarizer import TranscriptSummarizer  # ✅ Include this
from ai_model.inference import extract_action_items
from db.models import meetings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from celery_worker import celery_app

# DB setup
DATABASE_URL = "postgresql+psycopg2://dhyeypatel:Dhyey%402003@localhost/meetings_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def convert_gdrive_url_to_direct(url: str) -> str:
    match = re.search(r'/d/([^/]+)', url)
    if match:
        file_id = match.group(1)
        return f'https://drive.google.com/uc?export=download&id={file_id}'
    return url

def download_file_from_url(url: str, local_path: str) -> str:
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(local_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return local_path

@celery_app.task(name="tasks.transcription_task.transcribe_meeting_task")
def transcribe_meeting_task(meeting_id: str, file_url: str):
    session = SessionLocal()
    local_file_path = f"/tmp/{meeting_id}.mp4"

    try:
        print(f"Started transcription for meeting {meeting_id} with URL {file_url}")
        direct_url = convert_gdrive_url_to_direct(file_url)
        download_file_from_url(direct_url, local_file_path)

        transcript = transcribe_audio(local_file_path)
        summary = TranscriptSummarizer(transcript)  # ✅ Summarize transcript
        print("Generated summary:", summary)
        action_items = extract_action_items(transcript)
        action_text = "; ".join(action_items)

        session.execute(
            meetings.update().where(meetings.c.id == meeting_id).values(
                status="completed",
                transcript=transcript,
                summary=summary,  # ✅ Save summary
                action_items=action_text
            )
        )
        session.commit()

        print("Transcription, summary, and action item extraction completed!")

    except SQLAlchemyError as db_err:
        session.rollback()
        print("Database error:", db_err)
        session.execute(
            meetings.update().where(meetings.c.id == meeting_id).values(
                status="failed",
                transcript=str(db_err)
            )
        )
        session.commit()

    except Exception as e:
        session.rollback()
        print("General error:\n", e)
        session.execute(
            meetings.update().where(meetings.c.id == meeting_id).values(
                status="failed",
                transcript=str(e)
            )
        )
        session.commit()

    finally:
        if os.path.exists(local_file_path):
            os.remove(local_file_path)
        session.close()

