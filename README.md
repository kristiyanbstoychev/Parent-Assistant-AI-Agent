# AI Parenting Agent

A local AI-powered parenting advisor based on "How to Talk So Little Kids Will Listen" by Joanna Faber and Julie King. This agent provides evidence-based parenting advice optimized for low-resource systems (8GB RAM).

## Table of Contents
- [Overview](#overview)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [Examples](#examples)
- [Limitations](#limitations)

## Overview

This AI parenting agent combines:
- **Book-based knowledge**: Expert advice from "How to Talk So Little Kids Will Listen"
- **Web search capability**: Real-time information from the internet
- **ReAct agent architecture**: Reasoning and acting in an iterative loop
- **Memory-efficient design**: Optimized for 8GB RAM systems

### What It Does

The agent can:
1. Answer parenting questions using proven communication techniques
2. Provide age-appropriate advice for children 2-7 years old
3. Search the internet for current research when needed
4. Maintain context throughout conversations
5. Give actionable, practical recommendations

### Example Interactions

**User**: "My 4-year-old won't clean up their toys. What should I do?"

**Agent**: Uses book knowledge to suggest:
- Turning cleanup into a game
- Offering choices about which toys to clean first
- Using songs or timers as cues
- Acknowledging what the child does well

## System Requirements

### Hardware
- **RAM**: 8GB minimum (critical constraint)
- **Storage**: 5GB free space (for model and dependencies)
- **CPU**: Modern multi-core processor recommended

### Software
- **Operating System**: Linux, macOS, or Windows
- **Python**: 3.8 or higher
- **Ollama**: Latest version

### Network
- Internet connection required for:
  - Initial setup and model download
  - Web search functionality
  - Package installation

## Installation

### Step 1: Install Ollama

**Linux/macOS**:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows**:
Download installer from: https://ollama.com/download

Verify installation:
```bash
ollama --version
```

### Step 2: Pull the Qwen Model

```bash
ollama pull qwen2.5:3b
```

This downloads a 4-bit quantized model (approximately 2GB) optimized for 8GB RAM systems.

Verify the model:
```bash
ollama run qwen2.5:3b "Hello, test message"
```

### Step 3: Clone or Download This Project

```bash
# If using git
git clone <repository-url>
cd ai_parenting_agent

# Or download and extract the ZIP file
```

### Step 4: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies:
pip install langchain==0.3.13 langchain-community==0.3.13 langchain-core==0.3.28 ollama==0.4.4 duckduckgo-search==7.1.0 numpy==1.26.4
```

### Step 5: Verify Installation

Check that all files are present:
```
ai_parenting_agent/
├── parenting_agent.py      # Main application
├── book_summary.txt         # Knowledge base
├── requirements.txt         # Python dependencies
├── .gitignore              # Git exclusions
└── README.md               # This file
```

## Configuration

### Model Settings

Edit `parenting_agent.py` to adjust these parameters:

```python
# Line 54: Change the model
MODEL_NAME = "qwen2.5:3b"  # Default optimized for 8GB RAM

# Line 60: Adjust creativity
TEMPERATURE = 0.3  # Range: 0.0 (deterministic) to 1.0 (creative)
```

### Memory Management

The agent is configured for 8GB RAM systems:
- **Context window**: 4096 tokens (~3000 words)
- **Max iterations**: 5 (prevents runaway loops)
- **Model size**: 3B parameters (4-bit quantized)

### Book Summary

The knowledge base is stored in `book_summary.txt`. To update:
1. Edit the file with any text editor
2. Restart the agent to load changes
3. Keep content under 10,000 characters for optimal performance

## Usage

### Starting the Agent

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run the agent
python parenting_agent.py
```

### Conversation Flow

```
=======================================================================
AI PARENTING AGENT - Powered by 'How to Talk So Little Kids Will Listen'
=======================================================================

Loading parenting knowledge base...
Loaded 3847 characters of parenting guidance.

Initializing AI model (qwen2.5:3b)...
AI model ready.

Creating agent tools...
Created 2 tools: ['book_knowledge', 'web_search']

Assembling parenting agent...
Agent ready.

=======================================================================
You can now ask parenting questions.
Type 'quit', 'exit', or 'bye' to end the conversation.
=======================================================================

You: My child has tantrums when I say no. How do I handle this?
```

### Exiting

Type any of these commands to exit:
- `quit`
- `exit`
- `bye`

Or press `Ctrl+C` for immediate exit.

## Architecture

### Component Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                            │
│                   (Command Line)                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   AGENT EXECUTOR                             │
│              (Manages conversation flow)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  ReAct AGENT CORE                            │
│         (Reasoning + Acting in iterative loop)               │
└─────────┬─────────────────────────┬─────────────────────────┘
          │                         │
          ▼                         ▼
┌──────────────────────┐  ┌──────────────────────┐
│   BOOK KNOWLEDGE     │  │    WEB SEARCH        │
│       TOOL           │  │       TOOL           │
└──────────────────────┘  └──────────────────────┘
          │                         │
          ▼                         ▼
┌──────────────────────┐  ┌──────────────────────┐
│  book_summary.txt    │  │  DuckDuckGo API      │
└──────────────────────┘  └──────────────────────┘
          │                         │
          └────────────┬────────────┘
                       ▼
          ┌────────────────────────┐
          │   OLLAMA (qwen2.5:3b)  │
          │   (Language Model)     │
          └────────────────────────┘
                       │
                       ▼
          ┌────────────────────────┐
          │   FINAL RESPONSE       │
          └────────────────────────┘
```

### Tool Selection Logic

The agent follows this decision tree:

```
User Question
    │
    ▼
Is this a general parenting question?
    │
    ├─ YES → Use book_knowledge tool
    │         │
    │         ▼
    │    Is more context needed?
    │         │
    │         ├─ YES → Use web_search tool
    │         └─ NO → Generate response
    │
    └─ NO → Use web_search tool
              │
              ▼
         Generate response
```

### ReAct Loop Example

```
Input: "My child lies about eating candy"

Iteration 1:
  Thought: This is about lying, check the book
  Action: book_knowledge
  Observation: [Book content about truth-telling]

Iteration 2:
  Thought: I have good book advice, check for recent research
  Action: web_search
  Observation: [Web results about child development]

Iteration 3:
  Thought: I have enough information
  Final Answer: [Combined advice from book + web]
```

## Troubleshooting

### Common Issues

#### Issue: "Model not found"
**Symptom**: Error when starting agent
```
Error: model 'qwen2.5:3b' not found
```

**Solution**:
```bash
ollama pull qwen2.5:3b
ollama list  # Verify model is installed
```

#### Issue: "Out of memory" or system freeze
**Symptom**: Computer becomes slow or unresponsive

**Solution**:
1. Close other applications
2. Verify model size:
```bash
ollama list  # Should show qwen2.5:3b at ~2GB
```
3. If using a different model, switch to qwen2.5:3b

#### Issue: "Book summary not found"
**Symptom**: Error message at startup
```
Error: Book summary file not found at book_summary.txt
```

**Solution**:
1. Verify `book_summary.txt` exists in the same directory as `parenting_agent.py`
2. Check file permissions:
```bash
ls -l book_summary.txt
```

#### Issue: Web search not working
**Symptom**: "Error accessing web search"

**Solution**:
1. Check internet connection
2. Verify DuckDuckGo is accessible:
```bash
ping duckduckgo.com
```
3. Try disabling VPN if active

#### Issue: Slow responses
**Symptom**: Agent takes 30+ seconds to respond

**Causes and Solutions**:
1. **First response is always slow**: Model loading (expected)
2. **Consistent slowness**: 
   - Close background applications
   - Reduce context window in code (line 141: `num_ctx=2048`)
   - Consider upgrading RAM

### Debug Mode

To see detailed agent reasoning, the code already has `verbose=True` enabled. You'll see output like:

```
> Entering new AgentExecutor chain...
Thought: I should check the book for advice on this topic
Action: book_knowledge
Action Input: cooperation and cleanup
Observation: [Book content...]
```

### Performance Optimization

**For 8GB RAM systems**:
1. Close browser and other memory-intensive apps
2. Use the 3B model only (don't upgrade to larger models)
3. Keep conversations focused (avoid very long contexts)

**If you have 16GB+ RAM**:
Consider upgrading to a larger model:
```bash
ollama pull qwen2.5:7b
# Update MODEL_NAME in parenting_agent.py to "qwen2.5:7b"
```

## Examples

### Example 1: Handling Emotions

**User**: "My 3-year-old throws tantrums when frustrated. What should I do?"

**Agent Response**: 
```
Based on "How to Talk So Little Kids Will Listen," here's guidance for tantrums:

1. ACKNOWLEDGE FEELINGS FIRST
   - Get down to their level physically
   - Say: "I can see you're really upset right now"
   - Name the emotion: "You're feeling frustrated"

2. ALLOW SPACE FOR EXPRESSION
   - Don't rush to fix it
   - Let them cry or express anger safely
   - Stay calm and present

3. AFTER THE STORM
   - Use simple language: "You wanted the red cup, not blue"
   - Offer choices: "We can try again later" or "Let's take deep breaths"
   - Problem-solve together when calm

Remember: Feelings come first, behavior comes second. The tantrum is 
communication, not misbehavior.
```

### Example 2: Encouraging Cooperation

**User**: "Getting my 5-year-old ready for school is a daily battle"

**Agent Response**:
```
Let's make mornings easier using positive communication:

1. USE PLAYFULNESS
   - "I bet you can't put shoes on faster than I count to 10!"
   - Race: "Let's see if you can beat the timer"
   - Songs: Create a morning routine song together

2. OFFER CHOICES
   - "Do you want to brush teeth first or get dressed first?"
   - "Should we pack your blue bag or red bag today?"
   - This gives control without chaos

3. VISUAL CUES
   - Create a morning checklist with pictures
   - Use one-word reminders: "Shoes!" instead of lectures
   - Let them check off completed tasks

4. ACKNOWLEDGE EFFORT
   - "You put your jacket on all by yourself!"
   - Focus on what they DO right, not what they forget

Keep it simple, keep it fun. Children cooperate more when they feel 
respected and involved.
```

### Example 3: Combining Book + Web Search

**User**: "Is it normal for my 4-year-old to lie about breaking things?"

**Agent Response**:
```
Yes, this is developmentally normal. Here's why and what to do:

FROM THE BOOK:
- Describe what you observe: "I see the vase is broken"
- Don't accuse: Skip "Did you break this?"
- Share feelings: "I feel sad when things break"
- Problem-solve together: "How can we clean this up safely?"
- Acknowledge why they might lie: "Maybe you were worried I'd be angry"

RECENT RESEARCH (2024):
Children age 3-5 are developing understanding of truth vs. fantasy. 
Lying often stems from:
- Fear of punishment
- Magical thinking ("Maybe it didn't happen if I say it didn't")
- Testing boundaries
- Protecting someone they care about

PRACTICAL STEPS:
1. Make it safe to tell the truth
2. Focus on repair, not punishment
3. Model honesty yourself
4. Use storytelling to discuss honesty
5. Praise truth-telling: "Thank you for telling me what happened"

This phase typically decreases by age 6-7 as executive function develops.
```

## Limitations

### Technical Limitations

1. **Memory**: 8GB RAM restricts model size and context length
2. **Offline capability**: Web search requires internet connection
3. **Language**: English only (model limitation)
4. **Processing speed**: Local inference slower than cloud APIs

### Content Limitations

1. **Scope**: Best for children ages 2-7
2. **Complexity**: Not a replacement for therapy or medical advice
3. **Cultural context**: Based primarily on Western parenting research
4. **Personalization**: Doesn't know your specific family situation

### Safety Considerations

**This tool is NOT for**:
- Emergency situations
- Medical diagnoses
- Mental health crises
- Legal advice
- Situations involving abuse or neglect

**Always consult professionals for**:
- Developmental delays
- Behavioral disorders
- Family therapy needs
- Medical concerns

## Contributing

To improve this project:
1. Update the book summary with more detailed guidance
2. Add more sophisticated RAG (Retrieval Augmented Generation)
3. Implement conversation history persistence
4. Add multilingual support
5. Create a web interface

## License

This project is for educational purposes. The book content is summarized under fair use for personal reference.

## Acknowledgments

- Book: "How to Talk So Little Kids Will Listen" by Joanna Faber and Julie King
- Model: Alibaba Cloud (Qwen 2.5)
- Framework: LangChain
- Search: DuckDuckGo
- Runtime: Ollama

## Support

For issues:
1. Check [Troubleshooting](#troubleshooting) section
2. Verify all installation steps completed
3. Ensure Ollama service is running: `ollama list`
4. Check Python version: `python --version` (should be 3.8+)

## Version History

**v1.0.0** (Current)
- Initial release
- ReAct agent with book knowledge and web search
- Optimized for 8GB RAM
- Command-line interface

---

**Ready to start?** Run `python parenting_agent.py` and ask your first question!