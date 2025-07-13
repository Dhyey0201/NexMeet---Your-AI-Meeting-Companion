import aiofiles
import os

UPLOAD_DIR = "uploads"

async def save_upload_file(file, meeting_id: str):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_ext = file.filename.split(".")[-1]
    file_path = os.path.join(UPLOAD_DIR, f"{meeting_id}.{file_ext}")

    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    return file_path
