from fastapi import FastAPI, HTTPException
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from db.database import database
from routers import upload
from db.models import meetings
from db.database import database
from sqlalchemy import select

# CORS middleware setup
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = FastAPI(middleware=middleware)

# Connect to DB on startup
@app.on_event("startup")
async def startup():
    await database.connect()

# Disconnect on shutdown
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Upload endpoint
app.include_router(upload.router)

# ✅ New: GET /meetings — list all meetings
@app.get("/meetings")
async def list_meetings():
    query = select(meetings)
    results = database.fetch_all(query)
    return results

# ✅ New: GET /meetings/{meeting_id} — get meeting by ID
@app.get("/meetings/{meeting_id}")
async def get_meeting(meeting_id: str):
    query = select(meetings).where(meetings.c.id == meeting_id)
    result = database.fetch_one(query)
    if result is None:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return result
