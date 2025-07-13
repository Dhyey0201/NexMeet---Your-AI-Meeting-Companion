from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6380/0",
    backend="redis://localhost:6380/0",
    include=["services.meeting_processor"]  # important: include your task module here

)

celery_app.conf.imports = ["tasks.transcription_task"]
