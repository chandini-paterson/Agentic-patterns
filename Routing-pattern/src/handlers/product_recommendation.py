from src.handlers.base import BaseHandler
from src.models.responses import HandlerResponse
from src.models.routing import RoutingDecision

class ProductRecommendationHandler(BaseHandler):
    """Handles product recommendation requests"""
    
    def handle(self, query: str, routing_decision: RoutingDecision) -> HandlerResponse:
        system_prompt = """You are a product recommendation specialist.
        Help customers find products that match their needs.
        Ask about preferences, budget, and use cases when needed.
        Provide personalized recommendations with clear reasoning."""
        
        prompt = f"""Customer is looking for: {query}
        
        Please provide helpful product recommendations."""
        
        response = self._call_llm(prompt, system_prompt)
        
        return HandlerResponse(
            response=response,
            metadata={
                "category": "recommendation",
                "personalized": True
            },
            handler_name="ProductRecommendationHandler"
        )