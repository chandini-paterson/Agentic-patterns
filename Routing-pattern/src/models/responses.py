from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class HandlerResponse:
    """Response from a specialized handler"""
    response: str
    metadata: Dict[str, Any]
    handler_name: str