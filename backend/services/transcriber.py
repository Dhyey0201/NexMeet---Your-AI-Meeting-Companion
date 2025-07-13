import whisper
import os

model = whisper.load_model("base")

async def transcribe_audio(file_path: str) -> str:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")

    result = model.transcribe(file_path)
    text = result.get("text", "").strip()

    if not text:
        raise ValueError("Transcription failed: No text returned")

    return text
