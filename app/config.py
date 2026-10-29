import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings(BaseModel):
    PROJECT_NAME: str = "PG Finder - StaySathi Voice AI"
    VERSION: str = "1.0.0"
    
    # LLM Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai").lower()
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    
    # Speech
    DEFAULT_TTS_VOICE: str = os.getenv("DEFAULT_TTS_VOICE", "hi-IN-SwaraNeural")
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    
    # Storage
    STORAGE_DIR: Path = BASE_DIR / "storage"
    RECORDINGS_DIR: Path = BASE_DIR / "storage" / "recordings"
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'storage' / 'staysathi.db'}")

settings = Settings()

# Ensure storage directories exist
settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
settings.RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)

