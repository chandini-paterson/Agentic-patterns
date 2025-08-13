"""
Streamlit interface for the Routing Pattern demonstration
Run with: streamlit run app.py
"""

from typing import Dict

from datetime import datetime
import streamlit as st

# Import our routing components
from src.router.router import Router
from src.models.routing import QueryCategory
from src.config.settings import settings

# Page configuration
st.set_page_config(
    page_title="AI Routing Pattern Demo",
    page_icon="🔀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 20px;
        background-color: #f5f5f5;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .message-container {
        margin-bottom: 20px;
        padding: 15px;
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .query-text {
        font-weight: bold;
        color: #1976D2;
        margin-bottom: 10px;
    }
    .response-text {
        color: #333;
        margin-bottom: 10px;
    }
    .routing-metadata {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
        font-size: 0.9em;
    }
    .category-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.85em;
        margin-right: 10px;
    }
    .sample-question {
        background-color: #e8f4f8;
        padding: 8px 12px;
        margin: 5px 0;
        border-radius: 5px;
        cursor: pointer;
        font-size: 0.9em;
    }
    .sample-question:hover {
        background-color: #d0e8f0;
    }
    .input-container {
        position: sticky;
        bottom: 0;
        background-color: white;
        padding: 20px 0;
        border-top: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'router' not in st.session_state:
    st.session_state.router = Router(model_name=settings.OLLAMA_MODEL)
    
if 'messages' not in st.session_state:
    st.session_state.messages = []


# Sample questions organized by category
SAMPLE_QUESTIONS = {
    "General Inquiries": [
        "What are your business hours?",
        "Where are you located?",
        "Do you offer international shipping?",
        "What payment methods do you accept?"
    ],
    "Refund & Returns": [
        "I want to return my order #12345, it arrived damaged",
        "How long do I have to return an item?",
        "My package never arrived, can I get a refund?",
        "I received the wrong item in my order"
    ],
    "Technical Support": [
        "My app keeps crashing when I try to log in",
        "The website won't load on my browser",
        "I'm getting error code E404 on the screen",
        "How do I reset my password?"
    ],
    "Billing Questions": [
        "Why was I charged twice for my subscription?",
        "I don't recognize this charge on my card",
        "How can I update my payment method?",
        "When will I receive my invoice?"
    ],
    "Product Recommendations": [
        "Can you recommend a good laptop for programming?",
        "What's the best phone for photography?",
        "I need a gift for a 10-year-old, any suggestions?",
        "Which of your products is best for beginners?"
    ]
}

def get_category_color(category: QueryCategory) -> str:
    """Get color for category badge"""
    colors = {
        QueryCategory.GENERAL_INQUIRY: "#2196F3",
        QueryCategory.REFUND_REQUEST: "#FF9800",
        QueryCategory.TECHNICAL_SUPPORT: "#f44336",
        QueryCategory.BILLING_QUESTION: "#9C27B0",
        QueryCategory.PRODUCT_RECOMMENDATION: "#4CAF50",
        QueryCategory.UNKNOWN: "#757575"
    }
    return colors.get(category, "#757575")

def process_query(query_text: str) -> None:
    """Process a query and add to message history"""
    with st.spinner("Processing query..."):
        try:
            # Route the query
            response, routing_decision = st.session_state.router.route_query(query_text)
            
            # Add to messages
            st.session_state.messages.append({
                'timestamp': datetime.now(),
                'query': query_text,
                'response': response,
                'routing_decision': routing_decision
            })
            

            # Rerun to update the display
            st.rerun()
            
        except Exception as e:
            st.error(f"Error processing query: {str(e)}")

def display_message(message: Dict):
    """Display a single message in the chat history"""
    with st.chat_message("user"):
        st.markdown(f"{message['query']}")
    
    with st.chat_message("assistant"):
        st.markdown(f"{message['response'].response}")

        # Routing metadata
        col1, col2, col3, col4 = st.columns([2, 2, 2, 3])
        
        with col1:
            color = get_category_color(message['routing_decision'].category)
            category_name = message['routing_decision'].category.value.replace("_", " ").title()
            st.markdown(
                f'<span class="category-badge" style="background-color: {color}; color: white;">'
                f'{category_name}</span>',
                unsafe_allow_html=True
            )
        
        with col2:
            confidence = message['routing_decision'].confidence * 100
            st.write(f"📊 Confidence: {confidence:.1f}%")
        
        with col3:
            st.write(f"🔧 {message['response'].handler_name.replace('Handler', '')}")
        
        with col4:
            st.write(f"🕐 {message['timestamp'].strftime('%H:%M:%S')}")
        
        # Show reasoning and extracted info in expander
        with st.expander("View details"):
            st.write("**Reasoning:**", message['routing_decision'].reasoning)
            if message['routing_decision'].extracted_info and any(message['routing_decision'].extracted_info.values()):
                st.write("**Extracted Information:**")
                for key, value in message['routing_decision'].extracted_info.items():
                    if value and value != "if mentioned":
                        st.write(f"- {key.replace('_', ' ').title()}: {value}")

def main():
    # Header
    st.title("🔀 AI Routing Pattern Demo")
    st.markdown("""
    This demo showcases the **Routing Pattern** for AI agents. The system classifies incoming 
    customer service queries and routes them to specialized handlers for optimal responses.
    """)
    
    # Create layout with main content and sidebar
    col1, col2 = st.columns([3, 1])
    
    with col1:       
        for message in st.session_state.messages:
            display_message(message)

        # Chat input
        if prompt := st.chat_input("Say something"):
            with st.chat_message("user"):
                process_query(prompt) 


    with col2:
        st.subheader("📋 Sample Questions")
        st.markdown("Click any question to try it:")
        
        for category, questions in SAMPLE_QUESTIONS.items():
            with st.expander(category, expanded=False):
                for i, question in enumerate(questions):
                    if st.button(
                        question, 
                        key=f"sample_{category}_{i}",
                        use_container_width=True,
                        help=f"Click to send: {question}"
                    ):
                        process_query(question)
    
    # Sidebar with system information and statistics
    with st.sidebar:
        st.header("⚙️ System Information")
        st.info(f"**Model:** {settings.OLLAMA_MODEL}")
        st.info(f"**Confidence Threshold:** {settings.DEFAULT_CONFIDENCE_THRESHOLD}")
        
        if st.button("🗑️ Clear Conversation", type="secondary", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        st.header("ℹ️ About")
        st.markdown("""
        **Routing Pattern** classifies queries and routes them to specialized handlers:
        
        - ✅ Automatic classification
        - 🎯 Specialized responses
        - 📊 Confidence scoring
        - 🔍 Information extraction
        
        Based on Anthropic's guide on building effective AI agents.
        """)

if __name__ == "__main__":
    main()