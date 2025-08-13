from src.handlers.base import BaseHandler
from src.models.responses import HandlerResponse
from src.models.routing import RoutingDecision


class BillingQuestionHandler(BaseHandler):
    """Handles billing and payment related queries"""
    
    def handle(self, query: str, routing_decision: RoutingDecision) -> HandlerResponse:
        system_prompt = """You are a billing specialist.
        Handle questions about charges, invoices, payment methods, and billing cycles.
        Be precise with financial information and always maintain customer privacy.
        If specific account details are needed, explain what information you need and why."""
        
        prompt = f"""Billing question: {query}
        
        Please address this billing concern professionally."""
        print(f"routing decision: {routing_decision}    ")

        response = self._call_llm(prompt, system_prompt)
        
        return HandlerResponse(
            response=response,
            metadata={
                "category": "billing",
                "sensitive_data": True
            },
            handler_name="BillingQuestionHandler"
        )
