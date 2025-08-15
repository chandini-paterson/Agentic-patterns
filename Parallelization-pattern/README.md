# LLM Parallelization Patterns Demo

A Streamlit application demonstrating parallelization patterns for LLM workflows, based on Anthropic's guide "Building Effective Agents". This demo showcases two key parallelization patterns: **Sectioning** and **Voting**.

## Overview

This project implements two parallelization patterns:

1. **Sectioning Pattern**: Breaking complex tasks into independent subtasks that run in parallel
2. **Voting Pattern**: Running the same task multiple times with different approaches to achieve consensus

## Features

### 📰 Newsletter Generation (Sectioning)

- Generates AI-focused newsletters by creating multiple sections in parallel
- Sections include: Headlines, Technical Deep Dive, Industry News, Tools & Resources, and Opinion & Analysis
- All sections are generated simultaneously for faster results
- Output formatted as professional markdown newsletter

### 🎭 Sentiment Analysis (Voting)

- Analyzes text sentiment using multiple LLM calls with different prompts
- Three parallel analyzers vote on sentiment (POSITIVE, NEGATIVE, or NEUTRAL)
- Final result determined by majority vote
- Displays vote distribution and individual results for transparency

## Prerequisites

- Python 3.7+
- [Ollama](https://ollama.ai/) installed and running locally
- Gemma 3B model downloaded in Ollama

## Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd parallelization-demo
```

2. **Install Python dependencies**

```bash
pip install streamlit aiohttp
```

3. **Install and configure Ollama**

```bash
# Install Ollama (if not already installed)
# Visit https://ollama.ai for installation instructions

# Pull the Gemma 3B model
ollama pull gemma:3b

# Start Ollama server
ollama serve
```

## Usage

1. **Start the Streamlit application**

```bash
streamlit run parallelization_demo.py
```

2. **Open your browser**

   - The app will automatically open at `http://localhost:8501`

3. **Try the demos**
   - **Newsletter Tab**: Enter an AI-related topic (e.g., "Large Language Models", "Computer Vision")
   - **Sentiment Tab**: Paste any text to analyze its sentiment

## How It Works

### Sectioning Pattern

```python
# All sections generated in parallel
async def generate_newsletter_sections(topic: str):
    tasks = []
    for section, prompt in SECTION_PROMPTS.items():
        tasks.append(call_ollama(session, prompt))

    # Run all tasks simultaneously
    responses = await asyncio.gather(*tasks)
```

### Voting Pattern

```python
# Multiple prompts analyze the same text
async def analyze_sentiment_voting(text: str):
    tasks = []
    for prompt in SENTIMENT_PROMPTS:
        tasks.append(call_ollama(session, prompt))

    # Collect all votes and determine majority
    responses = await asyncio.gather(*tasks)
```

## Configuration

The application uses the following default configuration:

- **Ollama URL**: `http://localhost:11434/api/generate`
- **Model**: `gemma:3b`

To modify these settings, edit the constants at the top of `parallelization_demo.py`:

```python
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma:3b"
```

## Benefits of Parallelization

### Speed

- **Sequential processing**: 5 sections × 3 seconds = 15 seconds
- **Parallel processing**: All sections in ~3 seconds total

### Reliability (Voting)

- Reduces bias from single prompt variations
- Increases confidence through consensus
- Identifies edge cases where models disagree

## Troubleshooting

### Ollama Connection Error

- Ensure Ollama is running: `ollama serve`
- Check if Gemma model is installed: `ollama list`
- Verify Ollama is accessible at `http://localhost:11434`

### Model Not Found

- Install Gemma model: `ollama pull gemma:3b`
- Or modify `MODEL` constant to match your installed model

### Slow Performance

- Parallelization requires sufficient system resources
- Consider reducing the number of parallel tasks if needed
- Ensure Ollama has adequate memory allocation

## Project Structure

```
parallelization-demo/
├── parallelization_demo.py  # Main Streamlit application
├── README.md               # This file
└── requirements.txt        # Python dependencies (optional)
```

## Further Reading

- [Anthropic's Guide: Building Effective Agents](https://www.anthropic.com/news/building-effective-agents)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Streamlit Documentation](https://docs.streamlit.io)

## License

This project is for educational purposes, demonstrating patterns from Anthropic's public guide on building effective agents.

## Acknowledgments

Based on patterns and principles from Anthropic's "Building Effective Agents" guide by Erik Schluntz and Barry Zhang.
