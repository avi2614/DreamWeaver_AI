import os, json, asyncio
import re
from langchain_google_genai import ChatGoogleGenerativeAI

# Absolute imports via the app.* package path
from app.tools.image_gen import generate_image
from app.tools.tts import speak  # optional: comment out if you haven't implemented speak()

# ───────────────────────────────────────────────────────────
# 1. Initialise Gemini 1.5 Flash LLM
# ───────────────────────────────────────────────────────────
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest"),
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7,
)

# ───────────────────────────────────────────────────────────
# 2. Planner – break prompt into JSON tasks
# ───────────────────────────────────────────────────────────
async def plan(prompt: str) -> list[dict]:
    system_msg = (
        "You are a creative director AI. "
        "Given a user idea, output ONLY a valid JSON array of tasks, and NOTHING else. "
        "Do NOT use Markdown code blocks, do NOT use triple backticks, do NOT add any text before or after the JSON. "
        "Allowed types: image, narration, speak. "
        "Each task MUST have 'type' and 'content'.\n"
        "Example:\n"
        "[{\"type\": \"narration\", \"content\": \"Once upon a time...\"}, {\"type\": \"image\", \"content\": \"A dragon in a forest\"}]"
    )
    response = llm.invoke(f"{system_msg}\nUser: {prompt}")
    response_text = response.content if hasattr(response, 'content') else str(response)
    print("[DEBUG] LLM plan() raw response:", repr(response_text))
    if not response_text.strip():
        print("[ERROR] LLM plan() returned empty response. Check your Gemini API key and network.")
        return [{"type": "narration", "content": "[ERROR] LLM returned empty response. Check Gemini API key."}]
    # Robustly remove Markdown code block if present
    response_text = response_text.strip()
    if response_text.startswith("```"):
        response_text = re.sub(r"^```[a-zA-Z]*\s*", "", response_text)
        if response_text.endswith("```"):
            response_text = response_text[:-3]
    response_text = response_text.strip()
    try:
        return json.loads(response_text)
    except Exception as e:
        print(f"[ERROR] LLM plan() invalid JSON: {e}")
        return [{"type": "narration", "content": f"[ERROR] LLM returned invalid JSON: {e}"}]

# ───────────────────────────────────────────────────────────
# 3. Execute each task
# ───────────────────────────────────────────────────────────
async def run_task(task: dict) -> str:
    ttype   = task.get("type", "narration")
    content = task.get("content", "")

    if ttype == "image":
        return await generate_image(content)

    if ttype == "speak":
        return await speak(content)  # returns path to MP3

    # default: narration
    response = llm.invoke(content)
    response_text = response.content if hasattr(response, 'content') else str(response)
    print(f"[DEBUG] LLM run_task() raw response for type={ttype}:", repr(response_text))
    if not response_text.strip():
        print(f"[ERROR] LLM run_task() returned empty response for type={ttype}. Check Gemini API key.")
        return f"[ERROR] LLM returned empty response for type={ttype}. Check Gemini API key."
    return response_text

# ───────────────────────────────────────────────────────────
# 4. Public Agent class
# ───────────────────────────────────────────────────────────
class DreamWeaverAgent:
    async def run(self, prompt: str, mode: str = "story") -> dict:
        """
        Orchestrates plan → execute → returns results.

        Returns:
          {
            "mode": "story" | "comic" | "game",
            "assets": [ ... mixed: narration strings, data‑URL images, MP3 paths ... ]
          }
        """
        tasks    = await plan(prompt)
        results  = [await run_task(t) for t in tasks]
        return {"mode": mode, "assets": results}