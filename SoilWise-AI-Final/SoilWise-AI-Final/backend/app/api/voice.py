import base64
import binascii
from typing import Literal

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

from app.core.config import settings
from app.dependencies import current_user
from app.models.user import User

router = APIRouter()


class SpeechRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1800)
    language: Literal["hi-IN", "kn-IN"]


@router.post("/speech", response_class=Response)
async def speak_report(payload: SpeechRequest, _: User = Depends(current_user)):
    """Translate an English report excerpt and synthesize Hindi/Kannada speech."""
    if not settings.sarvam_api_key:
        raise HTTPException(status_code=503, detail="Voice service is not configured. Set SARVAM_API_KEY.")

    headers = {"api-subscription-key": settings.sarvam_api_key,
               "Content-Type": "application/json"}
    timeout = httpx.Timeout(35.0, connect=5.0)
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            translated = await client.post(
                "https://api.sarvam.ai/translate",
                headers=headers,
                json={"input": payload.text, "source_language_code": "en-IN",
                      "target_language_code": payload.language,
                      "model": "sarvam-translate:v1"},
            )
            translated.raise_for_status()
            translated_text = translated.json().get("translated_text", "").strip()
            if not translated_text:
                raise HTTPException(status_code=502, detail="Translation service returned an empty result.")
            speech = await client.post(
                "https://api.sarvam.ai/text-to-speech",
                headers=headers,
                json={"text": translated_text[:2500], "language_code": payload.language,
                      "model": "bulbul:v4-flash"},
            )
            speech.raise_for_status()
            audios = speech.json().get("audios") or []
            if not audios:
                raise HTTPException(status_code=502, detail="Speech service returned no audio.")
            audio_bytes = base64.b64decode(audios[0], validate=True)
    except HTTPException:
        raise
    except (httpx.TimeoutException, httpx.NetworkError):
        raise HTTPException(status_code=504, detail="Voice service timed out. Please try again.")
    except httpx.HTTPStatusError as exc:
        # Do not expose upstream response bodies, headers, or credentials to the client.
        status = exc.response.status_code
        if status == 429:
            raise HTTPException(status_code=429, detail="Voice service is busy. Please try again shortly.")
        raise HTTPException(status_code=502, detail="Voice generation failed. Check the Sarvam service configuration.")
    except (ValueError, KeyError, binascii.Error):
        raise HTTPException(status_code=502, detail="Voice service returned an invalid audio response.")

    return Response(content=audio_bytes, media_type="audio/wav",
                    headers={"Cache-Control": "private, no-store"})
