from src.handlers.base import BaseHandler
from src.models.responses import HandlerResponse
from src.models.routing import RoutingDecision

class GeneralInquiryHandler(BaseHandler):
    """Handles general questions and FAQs"""
    
    def handle(self, query: str, routing_decision: RoutingDecision) -> HandlerResponse:
        system_prompt = """You are a helpful customer service assistant handling general inquiries.
        Provide clear, concise, and friendly responses to common questions.
        If you don't know something, politely say so and offer to help find the information."""
        
        prompt = f"Customer query: {query}\n\nPlease provide a helpful response."
        
        response = self._call_llm(prompt, system_prompt)
        
        return HandlerResponse(
            response=response,
            metadata={"category": "general", "confidence": routing_decision.confidence},
            handler_name="GeneralInquiryHandler"
        )
