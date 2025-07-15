import os, httpx
import uuid
ELEVENLABS_KEY = os.getenv("ELEVENLABS_KEY")
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # (Default voice ID)

async def speak(text: str) -> str:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.7
        }
    }
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(url, headers=headers, json=data)
        resp.raise_for_status()
        audio_data = resp.content
        # Save to static directory with unique filename
        static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
        os.makedirs(static_dir, exist_ok=True)
        filename = f"tts_{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(static_dir, filename)
        with open(filepath, "wb") as f:
            f.write(audio_data)
        # Return the URL path for the frontend
        return f"/static/{filename}"
