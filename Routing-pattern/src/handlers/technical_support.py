from src.handlers.base import BaseHandler
from src.models.responses import HandlerResponse
from src.models.routing import RoutingDecision


class TechnicalSupportHandler(BaseHandler):
    """Handles technical support queries"""
    
    def handle(self, query: str, routing_decision: RoutingDecision) -> HandlerResponse:
        system_prompt = """You are a technical support specialist.
        Provide clear, step-by-step solutions to technical problems.
        Ask clarifying questions when needed to diagnose issues.
        Be patient and avoid using too much technical jargon."""
        
        prompt = f"""Technical issue: {query}
        
        Please provide troubleshooting steps or a solution."""
        
        response = self._call_llm(prompt, system_prompt)
        
        return HandlerResponse(
            response=response,
            metadata={
                "category": "technical",
                "may_need_escalation": routing_decision.confidence < 0.8
            },
            handler_name="TechnicalSupportHandler"
        )
