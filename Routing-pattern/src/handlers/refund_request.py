from src.handlers.base import BaseHandler
from src.models.responses import HandlerResponse
from src.models.routing import RoutingDecision

class RefundRequestHandler(BaseHandler):
    """Handles refund and return requests"""
    
    def handle(self, query: str, routing_decision: RoutingDecision) -> HandlerResponse:
        system_prompt = """You are a customer service specialist handling refund and return requests.
        Be empathetic and solution-oriented. Follow company policy:
        - Refunds are available within 30 days of purchase
        - Items must be in original condition
        - Customer needs order number and reason for return
        Always be polite and try to resolve issues satisfactorily."""
        
        # Extract any order information if available
        order_info = routing_decision.extracted_info.get("order_number", "Not provided")
        
        prompt = f"""Customer refund request: {query}
        
        Order number mentioned: {order_info}
        
        Please handle this refund request appropriately, asking for any missing information needed."""
        
        response = self._call_llm(prompt, system_prompt)
        
        return HandlerResponse(
            response=response,
            metadata={
                "category": "refund",
                "order_number": order_info,
                "requires_followup": True
            },
            handler_name="RefundRequestHandler"
        )