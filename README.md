# NexMeet 🎤🤖

NexMeet is an AI-powered meeting assistant that performs transcription, summarization, emotion detection, and action item extraction from meeting audio files.

## 🔧 Tech Stack

- **Frontend:** React + TailwindCSS
- **Backend:** FastAPI + PostgreSQL
- **AI:** Transcription, Summarization, Emotion Detection
- **Async Tasks:** Celery + Redis

## 🚀 How to Run Locally

1. Clone the repo:
git clone https://github.com/yourusername/NexMeet.git
cd NexMeet

markdown
Copy
Edit

2. Set up `.env` files in `frontend/` and `backend/`.

3. Start frontend:
cd frontend
npm install
npm run dev

markdown
Copy
Edit

4. Start backend:
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

markdown
Copy
Edit

5. Start Celery worker:
celery -A celery_worker.celery_app worker --loglevel=info

sql
Copy
Edit

6. (Optional) Start Redis if not running:
brew services # NexMeet---AI-Meeting-Companion
# NexMeet---AI-Meeting-Companion
