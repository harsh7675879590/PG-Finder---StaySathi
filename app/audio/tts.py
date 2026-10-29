import os
import uuid
import logging
from pathlib import Path
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self):
        self.default_voice = settings.DEFAULT_TTS_VOICE or "hi-IN-SwaraNeural"
        self.recordings_dir = settings.RECORDINGS_DIR
        self.recordings_dir.mkdir(parents=True, exist_ok=True)

    async def synthesize_speech(self, text: str, voice: Optional[str] = None) -> Optional[str]:
        """
        Synthesizes text into high-fidelity neural speech.
        Returns the relative web path to the generated audio file.
        Uses edge-tts (free neural voice, zero API key required).
        """
        voice = voice or self.default_voice
        filename = f"tts_{uuid.uuid4().hex[:12]}.mp3"
        filepath = self.recordings_dir / filename

        try:
            import edge_tts
            communicate = edge_tts.Communicate(text, voice=voice)
            await communicate.save(str(filepath))
            logger.info(f"Generated neural audio: {filepath.name} using voice: {voice}")
            return f"/storage/recordings/{filename}"
        except ImportError:
            logger.warning("edge-tts library not installed. Speech synthesis skipped.")
            return None
        except Exception as e:
            logger.error(f"TTS synthesis error: {e}")
            return None

tts_service = TTSService()
