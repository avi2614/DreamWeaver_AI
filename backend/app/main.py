from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.agents import DreamWeaverAgent
from dotenv import load_dotenv
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Serve static files (for audio, images, etc.)
app.mount("/static", StaticFiles(directory="app"), name="static")

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the agent instance
agent = DreamWeaverAgent()

# Route to handle AI storytelling/comic/game prompts
@app.post("/dream")
async def dream(request: Request):
    """
    Receives POST request with:
    {
      "prompt": "Describe a robot in a fantasy forest.",
      "mode": "comic"
    }
    Returns: { "mode": ..., "assets": [...] }
    """
    try:
        body = await request.json()
        prompt = body.get("prompt", "")
        mode = body.get("mode", "story")

        if not prompt:
            return {"error": "No prompt provided."}

        response = await agent.run(prompt, mode)
        return response
    except Exception as e:
        import traceback
        print("/dream error:", traceback.format_exc())
        return {"error": f"Server error: {str(e)}"}
