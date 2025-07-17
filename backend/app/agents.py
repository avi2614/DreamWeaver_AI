import os, json, asyncio
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from app.tools.image_gen import generate_image
from app.tools.tts import speak

llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest"),
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7,
)

def clean_llm_response(response):
    response_text = response.content if hasattr(response, 'content') else str(response)
    response_text = response_text.strip()
    if response_text.startswith("```"):
        response_text = re.sub(r"^```[a-zA-Z]*\s*", "", response_text)
        if response_text.endswith("```"):
            response_text = response_text[:-3]
    return response_text.strip()

class DreamWeaverAgent:
    async def run(self, prompt: str, mode: str = "story", word_count: int = None, language: str = None) -> dict:
        """
        For 'story': generate a story.
        For 'image': generate an image.
        For 'game': generate a mini-game code in the selected language using Gemini.
        Returns:
          {
            "mode": "story" | "image" | "game",
            "assets": [ ... ]
          }
        """
        if mode == "story":
            system_msg = (
                f"You are a master storyteller AI. Respond ONLY in {language.title()}. "
                "Given a prompt, write a creative, engaging, and clear story. "
                "Also explain the story like you are explaining it to a 12 year old child. The story should be 2 paragraphs. "
                "Avoid making the story long or confusing. Do NOT use Markdown or code blocks. Just return the story text."
            )
            if word_count:
                system_msg += f" The story should be close to {word_count} words."
            response = llm.invoke(f"{system_msg}\nUser: {prompt}")
            story = clean_llm_response(response)
            return {"mode": "story", "assets": [story]}
        elif mode == "image":
            image = await generate_image(prompt)
            return {"mode": "image", "assets": [image]}
        elif mode == "game":
            lang_map = {
                "python": "Python",
                "javascript": "JavaScript",
                "html": "HTML (with JavaScript)",
                "java": "Java",
                "csharp": "C#",
                "c": "C",
                "cpp": "C++"
            }
            lang_name = lang_map.get(language, "Python")
            system_msg = (
                f"You are an expert game developer AI. Respond ONLY in {language.title()}. Given a prompt, generate a playable mini-game as a single code file in {lang_name}. "
                f"The game should be simple, fun, and themed to the prompt. Output ONLY the {lang_name} code, no Markdown, no explanations. "
                f"Do NOT output HTML or JavaScript unless the selected language is HTML or JavaScript. If the user selects C, C++, Java, Python, or C#, output only valid code for that language."
            )
            response = llm.invoke(f"{system_msg}\nUser: {prompt}")
            game_code = clean_llm_response(response)
            return {"mode": "game", "assets": [game_code]}
        else:
            return {"mode": mode, "assets": [f"[ERROR] Unknown mode: {mode}"]}