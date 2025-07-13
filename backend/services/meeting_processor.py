from celery_worker import celery_app
from db.models import meetings
from db.database import database
from services.transcriber import transcribe_audio
from services.summarizer import TranscriptSummarizer
from services.emotion_detector import detect_emotion
from ai_model.inference import extract_action_items
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

@celery_app.task(name="services.meeting_processor.process_meeting", bind=True)
def process_meeting(self, meeting_id: str, file_path: str):
    logging.info(f"🧠 Celery: Processing meeting {meeting_id}")
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(async_process_meeting(meeting_id, file_path))

async def async_process_meeting(meeting_id: str, file_path: str):
    await database.connect()
    try:
        # Transcription
        transcript = await transcribe_audio(file_path)
        logging.info(f"📝 Transcript: {transcript[:100]}...")

        if not transcript.strip():
            raise ValueError("❌ Transcription returned empty text.")

        # 📚 Summary
        summarizer = TranscriptSummarizer()  # ✅ Create instance
        summary = summarizer.summarize_text(transcript)  # ✅ Use method
        logging.info(f"📚 Summary: {summary[:100]}...")


        # Emotion detection
        emotion = detect_emotion(file_path)
        logging.info(f"😠 Emotion: {emotion}")

        # Action items extraction (sync)
        action_items = extract_action_items(transcript)
        logging.info(f"📌 Action items: {action_items}")

        # Save results to DB
        query = meetings.update().where(meetings.c.id == meeting_id).values(
            transcript=transcript,
            summary=summary,
            emotion=emotion,
            action_items=action_items,
            status="processed"
        )


        await database.execute(query)
        logging.info(f"✅ Meeting {meeting_id} processed and saved.")
    except Exception as e:
        logging.error(f"❌ Error in async_process_meeting: {e}", exc_info=True)
        raise
    finally:
        await database.disconnect()
        logging.info("🔌 DB connection closed.")