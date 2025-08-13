## Routing Pattern

### Description

The Routing pattern is a workflow that classifies an input and directs it to a specialized follow-up task. It acts as an intelligent dispatcher that analyzes incoming requests and routes them to the most appropriate handler based on the content or characteristics of the input.

From Anthropic:  
<img width="907" height="393" alt="image" src="https://github.com/user-attachments/assets/82456eee-0ff1-409d-a407-e7f0825cf6fc" />


### Key Details

**Purpose**: The main goal of routing is to enable separation of concerns and build more specialized prompts for different types of inputs. Without routing, trying to optimize a single prompt for all types of inputs can hurt performance on specific cases.

**How it works**:

1. An initial classifier (either an LLM or traditional classification model) analyzes the input
2. Based on the classification, the input is directed to a specialized handler
3. Each handler is optimized for its specific type of input

**Benefits**:

- **Specialization**: Each route can have prompts and logic optimized for specific types of queries
- **Performance**: Can route simple queries to smaller, faster models and complex queries to more capable models
- **Cost optimization**: Use expensive models only when necessary
- **Maintainability**: Easier to update and improve individual routes without affecting others

### Common Examples

Based on the document, here are the main examples:

1. **Customer Service Routing**

   - General questions → FAQ handler
   - Refund requests → Refund processing system
   - Technical support → Technical specialist prompt
   - Billing inquiries → Billing system integration

2. **Model-Based Routing** (Cost/Performance Optimization)

   - Easy/common questions → Claude 3.5 Haiku (smaller, faster model)
   - Hard/unusual questions → Claude 3.5 Sonnet (more capable model)
   - This optimizes for both cost and speed while maintaining quality

3. **Domain-Specific Routing**

   - Legal questions → Legal expertise prompt
   - Medical questions → Medical knowledge handler
   - Technical questions → Programming assistant
   - Creative writing → Creative writing specialist

4. **Language Routing**

   - English queries → English-optimized handler
   - Other languages → Language-specific handlers or translation pipeline

5. **Intent-Based Routing**
   - Information seeking → Search and retrieval pipeline
   - Task execution → Action-oriented workflow
   - Conversation → Chatbot interaction flow

# Routing Pattern Implementation

This project demonstrates the Routing pattern for AI agents using Ollama and Gemma 3.

## Setup

1. Install Ollama: https://ollama.ai
2. Pull Gemma 3: `ollama pull gemma3`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and configure
5. Run: `python main.py` to run the command line version
   OR
   Run: `streamlit run app.py` to run the streamlit app with a UI chat interface

## Architecture

The routing pattern classifies incoming queries and routes them to specialized handlers:

- **Router**: Classifies queries and selects appropriate handlers
- **Handlers**: Specialized processors for different query types
- **LLM Client**: Wrapper for Ollama interactions

## Adding New Handlers

1. Create a new handler in `src/handlers/`
2. Inherit from `BaseHandler`
3. Add the category to `QueryCategory` enum
4. Register in the router's handler map
