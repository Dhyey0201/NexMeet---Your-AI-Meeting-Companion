from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import shutil
import uuid
import os
from db.models import meetings
from db.database import database
from services.meeting_processor import process_meeting  # Celery task

router = APIRouter()

@router.get("/meetings/{meeting_id}")
async def get_meeting(meeting_id: str):
    query = meetings.select().where(meetings.c.id == meeting_id)
    result = await database.fetch_one(query)  # ✅ FIXED: add await

    if not result:
        raise HTTPException(status_code=404, detail="Meeting not found")

    return result  # FastAPI will serialize this row to JSON automatically

@router.post("/meetings")
async def create_meeting(
    title: str = Form(...),
    file: UploadFile | None = File(None),
    file_url: str | None = Form(None),
):
    if file is None and file_url is None:
        raise HTTPException(status_code=400, detail="Must provide file or file_url")

    meeting_id = str(uuid.uuid4())  # ✅ Explicitly generate UUID

    if file:
        filename = f"{meeting_id}_{file.filename}"
        save_path = f"/tmp/{filename}"  # You can change this path
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        db_filename = filename
        db_file_url = None
    else:
        db_file_url = file_url
        db_filename = os.path.basename(file_url) or f"{meeting_id}.mp4"
        save_path = file_url

    # ✅ Insert into DB with generated UUID as `id`
    query = meetings.insert().values(
        id=meeting_id,
        title=title,
        filename=db_filename,
        file_url=db_file_url,
        stored_path=save_path,
        status="uploaded"
    )

    await database.execute(query)

    # ✅ Trigger Celery background task
    process_meeting.delay(meeting_id, save_path)

    return {
        "message": "✅ Meeting created & processing started",
        "meeting_id": meeting_id,
        "filename": db_filename,
        "file_url": db_file_url,
    }
