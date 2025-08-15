import asyncio
from typing import Tuple, List
import time
import aiohttp
import streamlit as st

# Ollama API configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma:3b"  # Adjust if your model name is different

# Sentiment analysis prompts for voting
SENTIMENT_PROMPTS = [
    """Analyze the sentiment of the following text. Respond with ONLY one word: POSITIVE, NEGATIVE, or NEUTRAL.
    Text: {text}""",
    
    """What is the emotional tone of this text? Reply with a single word only: POSITIVE, NEGATIVE, or NEUTRAL.
    Text: {text}""",
    
    """Classify the sentiment expressed in this text as either POSITIVE, NEGATIVE, or NEUTRAL. 
    Respond with only the classification word.
    Text: {text}"""
]

async def call_ollama(session: aiohttp.ClientSession, prompt: str) -> str:
    """Make an async call to Ollama API"""
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        async with session.post(OLLAMA_URL, json=payload) as ollama_response:
            if ollama_response.status == 200:
                ollama_result = await ollama_response.json()
                return ollama_result.get("response", "")
            else:
                return f"Error: Status {ollama_response.status}"
    except Exception as e:
        return f"Error: {str(e)}"

async def analyze_sentiment_voting(text: str) -> Tuple[str, List[str]]:
    """Analyze sentiment using multiple prompts and vote on result"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        for prompt_template in SENTIMENT_PROMPTS:
            prompt = prompt_template.format(text=text)
            tasks.append(call_ollama(session, prompt))
        
        # Run all sentiment analyses in parallel
        responses = await asyncio.gather(*tasks)
        
        # Clean and count votes
        sa_votes = []
        for sa_response in responses:
            # Extract just the sentiment word
            sa_sentiment = sa_response.strip().upper()
            if "POSITIVE" in sa_sentiment:
                sa_votes.append("POSITIVE")
            elif "NEGATIVE" in sa_sentiment:
                sa_votes.append("NEGATIVE")
            elif "NEUTRAL" in sa_sentiment:
                sa_votes.append("NEUTRAL")
            else:
                # If unclear, try to parse the first word
                first_word = sa_sentiment.split()[0] if sa_sentiment else ""
                if first_word in ["POSITIVE", "NEGATIVE", "NEUTRAL"]:
                    sa_votes.append(first_word)
        
        # Determine winner by majority vote
        if sa_votes:
            sa_vote_counts = {}
            for sa_vote in sa_votes:
                sa_vote_counts[sa_vote] = sa_vote_counts.get(sa_vote, 0) + 1
            
            winner = max(sa_vote_counts.items(), key=lambda x: x[1])[0]
            return winner, sa_votes
        else:
            return "UNABLE TO DETERMINE", sa_votes


# Streamlit UI
st.set_page_config(page_title="Parallelization Pattern Demo", page_icon="🚀", layout="wide")

st.title("LLM Parallelization Patterns Demo")
st.markdown("Demonstrating **Sectioning** and **Voting** parallelization patterns using Ollama and Gemma 3")

# Create tabs
tab1, tab2 = st.tabs(["🎭 Sentiment Analysis (Voting)",""])


# Tab: Sentiment Analysis (Voting)
with tab1:
    st.header("Sentiment Analysis using Voting")
    st.markdown("""
    This demonstrates the **voting** pattern where multiple LLM instances analyze the same text:
    - 3 different prompts analyze sentiment
    - Each "votes" for POSITIVE, NEGATIVE, or NEUTRAL
    - Final result is determined by majority vote
    
    This approach increases reliability by reducing single-prompt bias.
    """)
    
    text_to_analyze = st.text_area("Enter text for sentiment analysis:", 
                                  placeholder="Paste any text here to analyze its sentiment...",
                                  height=150)
    
    if st.button("Analyze Sentiment", key="sentiment_btn"):
        if text_to_analyze:
            with st.spinner("Running parallel sentiment analysis..."):
                start_time = time.time()
                
                # Run async function
                result, votes = asyncio.run(analyze_sentiment_voting(text_to_analyze))
                
                end_time = time.time()
                analysis_time = end_time - start_time
                
                # Display results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Final Sentiment", result)
                    st.success(f"✅ Analysis completed in {analysis_time:.2f} seconds")
                
                with col2:
                    st.subheader("Individual Votes")
                    for i, vote in enumerate(votes, 1):
                        st.write(f"Analyzer {i}: **{vote}**")
                
                # Show vote distribution
                if votes:
                    vote_counts = {}
                    for vote in votes:
                        vote_counts[vote] = vote_counts.get(vote, 0) + 1
                    
                    st.subheader("Vote Distribution")
                    for sentiment, count in vote_counts.items():
                        percentage = (count / len(votes)) * 100
                        st.progress(percentage / 100, text=f"{sentiment}: {count}/{len(votes)} ({percentage:.0f}%)")
        else:
            st.warning("Please enter text to analyze")

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About this Demo")
    st.markdown("""
    This demo showcases one of the two parallelization patterns from Anthropic's guide on building effective agents:
    
    **1. Voting Pattern**
    - Runs same task multiple times
    - Uses different approaches/prompts
    - Aggregates results for higher confidence
    
    **Requirements:**
    - Ollama running locally
    - Gemma 3 model installed
    - Python packages: streamlit, aiohttp
    """)
    
    st.header("🔧 Configuration")
    st.code(f"""
Model: {MODEL}
Endpoint: {OLLAMA_URL}
    """)
    
    if st.button("Test Ollama Connection"):
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            if response.status_code == 200:
                st.success("✅ Ollama is running!")
                models = response.json().get("models", [])
                if models:
                    st.write("Available models:")
                    for model in models:
                        st.write(f"- {model['name']}")
            else:
                st.error("❌ Ollama responded but with an error")
        except:
            st.error("❌ Cannot connect to Ollama. Make sure it's running!")