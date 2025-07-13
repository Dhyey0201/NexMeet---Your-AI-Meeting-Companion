import uuid
from sqlalchemy import Table, Column, String, DateTime, MetaData, Text
from datetime import datetime

metadata = MetaData()

meetings = Table(
    "meetings",
    metadata,
    Column("id", String, primary_key=True, default=lambda: str(uuid.uuid4())),
    Column("filename", String),
    Column("title", String),       # Add this
    Column("file_url", String),    # Add this
    Column("stored_path", String),
    Column("status", String, default="uploaded"),
    Column("transcript", Text),
    Column("summary", Text),
    Column("emotion", Text),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("action_items", Text),
)

