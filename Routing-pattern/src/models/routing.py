from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any

class QueryCategory(Enum):
    GENERAL_INQUIRY = "general_inquiry"
    REFUND_REQUEST = "refund_request"
    TECHNICAL_SUPPORT = "technical_support"
    BILLING_QUESTION = "billing_question"
    PRODUCT_RECOMMENDATION = "product_recommendation"
    UNKNOWN = "unknown"

@dataclass
class RoutingDecision:
    category: QueryCategory
    confidence: float
    reasoning: str
    extracted_info: Dict[str, Any]