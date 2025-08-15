import asyncio
from typing import Dict
from datetime import datetime
import time
import aiohttp
import streamlit as st

# Ollama API configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3"  # Adjust if your model name is different

# Newsletter section prompts
SECTION_PROMPTS = {
    "headlines": """Generate 3-4 attention-grabbing headlines about {topic} in AI. 
    Format as a bullet list. Be concise and impactful. Focus on recent developments and breakthroughs.  List your sources as links. 
    IMPORTANT: Provide ONLY the requested headlines. Do not add any questions, offers for more content, or additional commentary""",
    
    "technical_deep_dive": """Write a technical deep dive section about {topic} in AI.
    Include technical details, architecture, algorithms, or implementation details.
    Keep it informative but accessible. About 2-3 paragraphs.
    IMPORTANT: Provide ONLY the technical content. Do not add any questions, offers for more information, or additional commentary.""",
    
    "industry_news": """Write about recent industry news and business developments related to {topic} in AI.
    Include company announcements, partnerships, investments, or market trends.
    Format as 2-3 short news items.
    IMPORTANT: Provide ONLY the news content. Do not add any questions, offers for more content, or additional commentary.""",
    
    "tools_resources": """List 3-5 practical tools, libraries, or resources related to {topic} in AI.
    Include brief descriptions and why they're useful. Format as a bullet list.
    IMPORTANT: Provide ONLY the tools and resources list. Do not add any questions, offers for more suggestions, or additional commentary""",
    
    "opinion_analysis": """Provide thoughtful analysis and future outlook on {topic} in AI.
    Include potential impacts, challenges, and opportunities. Write 1-2 paragraphs with forward-looking perspective.
    IMPORTANT: Provide ONLY the analysis. Do not add any questions, offers for more perspectives, or additional commentary."""
}

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
                result = await ollama_response.json()
                return result.get("response", "")
            else:
                return f"Error: Status {ollama_response.status}"
    except Exception as e:
        return f"Error: {str(e)}"

async def generate_newsletter_sections(user_topic: str) -> Dict[str, str]:
    """Generate all newsletter sections in parallel"""
    print('in generate newsletter_sections')
    async with aiohttp.ClientSession() as session:
        tasks = []
        section_names = []
        
        for prompt_section, prompt_template in SECTION_PROMPTS.items():
            prompt = prompt_template.format(topic=user_topic)
            print(f"The prompt is {prompt} and section is {prompt_section}")
            tasks.append(call_ollama(session, prompt))
            section_names.append(prompt_section)
        
        print(f"Generated {len(tasks)} tasks for sections: {section_names}")
        # Run all section generations in parallel
        responses = await asyncio.gather(*tasks)
        
        # Combine results
        results = {}
        for result_section, result in zip(section_names, responses):
            print(f"Section: {result_section}, Response: {result}")
            results[result_section] = result
        
        print('in generate newsletter_sections, returning results')
        return results


def format_newsletter(user_topic: str, topic_sections: Dict[str, str]) -> str:
    """Format the newsletter sections into markdown"""
    print(f"in format_newsletter with topic: {user_topic} and sections: {topic_sections}")

    newsletter = f"""# AI Newsletter: {user_topic}
*Generated on {datetime.now().strftime('%B %d, %Y')}*

---

## 📰 Headlines

{topic_sections.get('headlines', 'No headlines generated.')}

---

## 🔬 Technical Deep Dive

{topic_sections.get('technical_deep_dive', 'No technical content generated.')}

---

## 🏢 Industry News

{topic_sections.get('industry_news', 'No industry news generated.')}

---

## 🛠️ Tools & Resources

{topic_sections.get('tools_resources', 'No tools/resources generated.')}

---

## 💭 Analysis & Outlook

{topic_sections.get('opinion_analysis', 'No analysis generated.')}

---

*This newsletter was generated using parallel AI processing, with each section created simultaneously by separate LLM instances.*
"""
    print('in format_newsletter, returning newsletter')
    return newsletter

# Streamlit UI
st.set_page_config(page_title="Parallelization Pattern Demo", page_icon="🚀", layout="wide")

st.title("LLM Parallelization Patterns Demo")
st.markdown("Demonstrating **Sectioning** and **Voting** parallelization patterns using Ollama and Gemma 3")

st.header("Newsletter Generation using Sectioning")
st.markdown("""
This demonstrates the **sectioning** pattern where we break down newsletter creation into parallel tasks:
- Headlines
- Technical Deep Dive
- Industry News
- Tools & Resources
- Opinion & Analysis
    
All sections are generated simultaneously for faster results.
""")
    
topic = st.text_input("Enter an AI topic for the newsletter:", 
                     placeholder="e.g., Large Language Models, Computer Vision, Reinforcement Learning")
    
if st.button("Generate Newsletter", key="newsletter_btn"):
    if topic:
        with st.spinner("Generating newsletter sections in parallel..."):
            start_time = time.time()

            print(f"Going to call generate newsletter sections for topic: {topic}")  
            # Run async function
            sections = asyncio.run(generate_newsletter_sections(topic))
            print(f"Finished calling generate newsletter sections for topic: {topic} and got sections: {sections}")
            end_time = time.time()
            generation_time = end_time - start_time
                
            # Display the formatted newsletter
            newsletter_content = format_newsletter(topic, sections)
            st.markdown(newsletter_content)
                
            # Show generation details
            st.success(f"✅ Newsletter generated in {generation_time:.2f} seconds using parallel processing")

            # Show sections in expander for debugging
            with st.expander("View raw section outputs"):
                for section, content in sections.items():
                    st.subheader(section.replace("_", " ").title())
                    st.text(content)   
    else:
        st.warning("Please enter a topic for the newsletter")



# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About this Demo")
    st.markdown("""
    This demo showcases one of the two parallelization patterns from Anthropic's guide on building effective agents:
    
    **1. Sectioning Pattern**
    - Breaks complex tasks into independent subtasks
    - Runs all subtasks simultaneously
    - Aggregates results into final output

    
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