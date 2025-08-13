"""
Main entry point for the Routing Pattern demonstration
"""

from src.router.router import Router


def demonstrate_routing():
    """Demonstrate the routing pattern with various example queries"""
    
    # Initialize the router
    router = Router()
    
    # Example queries representing different categories
    test_queries = [
        "What are your business hours?",
        "I want to return my order #12345, it arrived damaged",
        "My app keeps crashing when I try to log in",
        "Why was I charged twice for my subscription?",
        "Can you recommend a good laptop for programming?",
        "The screen is showing error code E404",
        "I need help choosing between your premium and basic plans",
    ]
    
    print("=" * 80)
    print("ROUTING PATTERN DEMONSTRATION")
    print("=" * 80)
    
    for query in test_queries:
        print(f"\n{'='*80}")
        print(f"QUERY: {query}")
        print("-" * 80)
        
        response, routing_decision = router.route_query(query)
        
        print("ROUTING DECISION:")
        print(f"  Category: {routing_decision.category.value}")
        print(f"  Confidence: {routing_decision.confidence:.2f}")
        print(f"  Reasoning: {routing_decision.reasoning}")
        if routing_decision.extracted_info:
            print(f"  Extracted Info: {routing_decision.extracted_info}")
        
        print(f"\nHANDLER: {response.handler_name}")
        print("\nRESPONSE:")
        print(f"{response.response}")
        
        if response.metadata:
            print(f"\nMETADATA: {response.metadata}")


if __name__ == "__main__":
    # Run the demonstration
    demonstrate_routing()