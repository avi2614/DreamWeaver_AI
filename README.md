# DreamWeaver_AI

DreamWeaver_AI is a full-stack, AI-powered creative toolkit that allows users to generate stories, images, and playable mini-games from prompts using state-of-the-art models. The project features a modern web UI and a Python FastAPI backend, with support for advanced image generation, code generation, and text-to-speech.

---

## Features

- **AI Story Generator:** Write a story from a user prompt.
- **AI Image Generator:** Create images from text using Replicate's API.
- **Game Code Generator:** Create playable mini-games in a selected programming language (Python, JavaScript, etc.) based on a prompt.
- **Text-to-Speech:** Convert generated stories into speech.
- **Modern Frontend:** Responsive UI powered by TailwindCSS and vanilla JS.

## Tech Stack

- **Backend:** Python, FastAPI, async tools, Replicate API, TTS, environment variable support.
- **Frontend:** HTML, TailwindCSS, JavaScript.
- **Deployment:** Dockerfiles provided for backend.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/avi2614/DreamWeaver_AI.git
cd DreamWeaver_AI
```

### 2. Backend Setup

- Edit `.env` in `/backend` to add your API keys (e.g., `REPLICATE_API_TOKEN`).
- Build and run with Docker:

```bash
cd backend
docker build -t dreamweaver-backend .
docker run -p 8000:8000 --env-file .env dreamweaver-backend
```

Or run locally with Python:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup

Just open `frontend/index.html` in your browser. Make sure the backend is running and accessible at `http://localhost:8000`.

---

## Usage

- **Story Tab:** Enter a prompt to generate a narrative.
- **Image Tab:** Enter a prompt to generate an image.
- **Game Tab:** Enter a prompt, select a language, and get source code for a mini-game (with 1-click copy).

---

## File Structure

```
backend/
  app/
    main.py          # FastAPI entrypoint
    agents.py        # AI agent logic for prompt handling
    tools/           # Image generation, TTS, etc.
  Dockerfile
frontend/
  index.html         # Main UI
  scripts/
    main.js          # UI logic and backend API calls
  styles.css         # Styling (via TailwindCSS)
```

---

## Environment Variables

Create a `.env` file in `backend/` with:

```
REPLICATE_API_TOKEN=your_replicate_token
# Optionally, set REPLICATE_MODEL and REPLICATE_VERSION
```

---

## Credits

- [Replicate](https://replicate.com/) for image generation API
- [FastAPI](https://fastapi.tiangolo.com/) for backend
- [TailwindCSS](https://tailwindcss.com/) for frontend styling

---

## License

MIT

---

## Author

[avi2614](https://github.com/avi2614)
