from abc import ABC, abstractmethod
import ollama
from src.utils.logging_config import logger
from src.models.responses import HandlerResponse
from src.models.routing import RoutingDecision


class BaseHandler(ABC):
    """Abstract base class for specialized handlers"""
    
    def __init__(self, model_name: str = "gemma3"):
        self.model_name = model_name
        self.client = ollama
    
    @abstractmethod
    def handle(self, query: str, routing_decision: RoutingDecision) -> HandlerResponse:
        """Process the query and return a response"""
        

    def _call_llm(self, prompt: str, system_prompt: str = "") -> str:
        """Helper method to call Ollama"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=messages
            )
            return response['message']['content']
        except Exception as e:
            logger.error("Error calling Ollama: %s", str(e))
           