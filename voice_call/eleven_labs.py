import requests
import base64
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

ELEVEN_LABS_API_KEY = "sk_f5f22e46a0bb22cce0c1ac66f2dc25f885342664d7787821"
ELEVEN_LABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"

def text_to_speech(text, voice_id="21m00Tcm4TlvDq8ikWAM"):  # Rachel voice
    """
    Convert text to speech using Eleven Labs API
    Returns base64 encoded audio data
    """
    try:
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVEN_LABS_API_KEY
        }

        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        logger.info(f"Sending request to Eleven Labs API for text: {text[:50]}...")
        response = requests.post(
            f"{ELEVEN_LABS_API_URL}/{voice_id}",
            json=data,
            headers=headers
        )

        if response.status_code == 200:
            logger.info("Successfully received audio from Eleven Labs API")
            return base64.b64encode(response.content).decode('utf-8')
        else:
            error_msg = f"Eleven Labs API error: Status {response.status_code}, Response: {response.text}"
            logger.error(error_msg)
            raise Exception(error_msg)
    except Exception as e:
        logger.error(f"Error in text_to_speech: {str(e)}")
        raise 