import os, httpx, base64

REPLICATE_API_TOKEN = "REPLICATE_API_TOKEN"  # Provided by user
REPLICATE_MODEL = "fast-flux-trainer"
# If you have a version ID, set it here. Otherwise, leave as None and use only the model slug.
REPLICATE_VERSION = None  # e.g., "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

async def generate_image(prompt: str):
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "version": REPLICATE_VERSION,
        "input": {"prompt": prompt}
    } if REPLICATE_VERSION else {
        "model": REPLICATE_MODEL,
        "input": {"prompt": prompt}
    }
    try:
        async with httpx.AsyncClient(timeout=120) as client:
            r = await client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            prediction = r.json()
            prediction_id = prediction["id"]
            # Poll for completion
            status = prediction["status"]
            while status not in ("succeeded", "failed", "canceled"):
                poll = await client.get(f"{url}/{prediction_id}", headers=headers)
                poll.raise_for_status()
                prediction = poll.json()
                status = prediction["status"]
            if status != "succeeded":
                return f"[ERROR] Replicate image generation failed: {status}"
            image_url = prediction["output"][0] if prediction["output"] else None
            if not image_url:
                return "[ERROR] No image returned from Replicate."
            # Download image and convert to data URL
            img_resp = await client.get(image_url)
            img_resp.raise_for_status()
            img_bytes = img_resp.content
            img_b64 = base64.b64encode(img_bytes).decode()
            return f"data:image/png;base64,{img_b64}"
    except Exception as e:
        print(f"[ERROR] Exception in generate_image (Replicate): {e}")
        return f"[ERROR] Image generation failed: {e}"
