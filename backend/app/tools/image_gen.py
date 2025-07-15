import os, httpx

HF = os.getenv("HF_SD_ENDPOINT")
HEADERS = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
print("[DEBUG] HF_SD_ENDPOINT:", HF)
print("[DEBUG] HF_TOKEN:", os.getenv('HF_TOKEN'))

async def generate_image(prompt: str):
    payload = {"inputs": prompt, "options": {"num_inference_steps": 30}}
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(HF, headers=HEADERS, json=payload)
            print("[DEBUG] HuggingFace response status:", r.status_code)
            print("[DEBUG] HuggingFace response text:", r.text[:500])
            r.raise_for_status()
            data = r.json()
            if "generated_images" in data and data["generated_images"]:
                image_b64 = data["generated_images"][0]
                return f"data:image/png;base64,{image_b64}"
            else:
                print("[ERROR] No generated_images in HuggingFace response.")
                return "[ERROR] No image generated. Check your HuggingFace quota, token, or model access."
    except Exception as e:
        print(f"[ERROR] Exception in generate_image: {e}")
        return f"[ERROR] Image generation failed: {e}"
