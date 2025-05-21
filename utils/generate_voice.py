import aiohttp
from settings.project_settings import Settings

settings = Settings()
ELEVEN_LABS_API_KEY = settings.eleven_labs_api_key
VOICE_ID = settings.eleven_labs_voice_id

async def synth_request_eleven_labs(text: str) -> bytes:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}?output_format=pcm_24000"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_LABS_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5,
        }
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            bytes = await response.read()
    return bytes