import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Ollama settings
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    
    # Router settings
    DEFAULT_CONFIDENCE_THRESHOLD = float(os.getenv("DEFAULT_CONFIDENCE_THRESHOLD", "0.7"))
    ENABLE_FALLBACK_HANDLER = os.getenv("ENABLE_FALLBACK_HANDLER", "true").lower() == "true"
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/routing.log")

settings = Settings()