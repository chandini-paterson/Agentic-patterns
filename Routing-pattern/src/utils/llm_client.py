from typing import List, Dict
import logging
import ollama
from src.utils.logging_config import logger 

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, model_name: str = "llama3", host: str = None):
        self.model_name = model_name
        self.client = ollama.Client(host=host) if host else ollama
    
    def chat(self, messages: List[Dict[str, str]]) -> str:
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=messages
            )
            return response['message']['content']
        except Exception as e:
            logger.error("Error calling Ollama: %s", str(e)) 
            raise