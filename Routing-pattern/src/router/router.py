from typing import Tuple
import json
import ollama
from src.utils.logging_config import logger
from src.models.routing import QueryCategory, RoutingDecision
from src.handlers.general_inquiry import GeneralInquiryHandler
from src.handlers.refund_request import RefundRequestHandler
from src.handlers.technical_support import TechnicalSupportHandler
from src.handlers.billing_question import BillingQuestionHandler 
from src.handlers.product_recommendation import ProductRecommendationHandler 
from src.models.responses import HandlerResponse


class Router:
    """Main routing class that classifies queries and routes to appropriate handlers"""
    
    def __init__(self, model_name: str = "gemma3"):
        self.model_name = model_name
        self.client = ollama
        
        # Initialize handlers
        self.handlers = {
            QueryCategory.GENERAL_INQUIRY: GeneralInquiryHandler(model_name),
            QueryCategory.REFUND_REQUEST: RefundRequestHandler(model_name),
            QueryCategory.TECHNICAL_SUPPORT: TechnicalSupportHandler(model_name),
            QueryCategory.BILLING_QUESTION: BillingQuestionHandler(model_name),
            QueryCategory.PRODUCT_RECOMMENDATION: ProductRecommendationHandler(model_name),
        }
        
        # Default handler for unknown categories
        self.default_handler = GeneralInquiryHandler(model_name)
    
    def classify_query(self, query: str) -> RoutingDecision:
        """Classify the query into one of the defined categories"""
        
        classification_prompt = f"""Classify the following customer service query into exactly ONE of these categories:

1. general_inquiry - General questions, FAQs, company information
2. refund_request - Requests for refunds, returns, or exchanges
3. technical_support - Technical problems, bugs, or issues with products/services
4. billing_question - Questions about charges, invoices, or payment methods
5. product_recommendation - Requests for product suggestions or comparisons

Also extract any relevant information like order numbers, product names, or error messages.

Query: "{query}"

Respond with a JSON object in this exact format:
{{
    "category": "one of the categories above",
    "confidence": 0.0 to 1.0,
    "reasoning": "brief explanation of why this category was chosen",
    "extracted_info": {{
        "order_number": "if mentioned",
        "product_name": "if mentioned",
        "error_message": "if mentioned"
    }}
}}

IMPORTANT: Respond ONLY with the JSON object, no additional text."""

        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": classification_prompt}]
            )
            
            # Parse the JSON response
            content = response['message']['content']
            # Clean up the response if it contains markdown
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            result = json.loads(content)
            
            # Map string category to enum
            category_str = result.get("category", "unknown")
            try:
                category = QueryCategory(category_str)
            except ValueError:
                category = QueryCategory.UNKNOWN
            
            return RoutingDecision(
                category=category,
                confidence=float(result.get("confidence", 0.5)),
                reasoning=result.get("reasoning", ""),
                extracted_info=result.get("extracted_info", {})
            )
            
        except (json.JSONDecodeError, KeyError) as e:
            logger.error("Error parsing classification response: %s", str(e))
            return RoutingDecision(
                category=QueryCategory.UNKNOWN,
                confidence=0.0,
                reasoning=f"Classification failed: {str(e)}",
                extracted_info={}
            )
    
    def route_query(self, query: str) -> Tuple[HandlerResponse, RoutingDecision]:
        """Main routing method - classifies and routes the query"""
        
        logger.info("Routing query: %s ", query[:50]) 
        
        # Step 1: Classify the query
        routing_decision = self.classify_query(query)
        logger.info("Classification: %s  (confidence: %s)", routing_decision.category.value, routing_decision.confidence)
        
        # Step 2: Route to appropriate handler
        handler = self.handlers.get(routing_decision.category, self.default_handler)
        
        # Step 3: Process with the selected handler
        response = handler.handle(query, routing_decision)
        
        return response, routing_decision

