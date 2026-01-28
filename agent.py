"""
AI Parenting Agent - Main Application Script

This script creates a helpful parenting assistant that gives advice based on the book
"How to Talk So Little Kids Will Listen". Think of it like having a friendly parenting
expert available 24/7 who has read this book and can also search the internet for you.

What this program does:
1. Reads the book summary (like reading a recipe book before cooking)
2. Connects to a small AI brain that runs on your computer (qwen3)
3. Can search the internet when needed (like asking Google for help)
4. Answers your parenting questions using the book's advice

Example: If you ask "My child won't clean up their toys", it will:
- First check the book summary for cleanup advice
- Maybe search online for more specific tips
- Give you a helpful answer combining both sources
"""

# =============================================================================
# IMPORTS - Loading the Tools We Need
# =============================================================================
# Think of imports like gathering ingredients before cooking

import os  # This helps us work with files and folders on the computer
from typing import List, Dict, Any  # This helps us organize our data neatly

# LangChain tools - These are like building blocks for our AI agent
from langchain.agents import AgentExecutor, create_react_agent  # The brain of our agent
from langchain_core.tools import Tool  # Lets us create custom abilities for the agent
from langchain_community.llms import Ollama  # Connects to the qwen3 AI model
from langchain_community.tools import DuckDuckGoSearchRun  # Internet search ability
from langchain_core.prompts import PromptTemplate  # Instructions template for the AI


# =============================================================================
# CONFIGURATION - Settings for the AI Agent
# =============================================================================
# These are the main settings we can change if needed

# Name of the AI model we're using (must be already installed in Ollama)
MODEL_NAME = "qwen3:8b"  

# Path to the book summary file (where our parenting wisdom lives)
BOOK_SUMMARY_PATH = "book_summary.txt"

# Temperature controls creativity vs consistency
# 0.3 means: "Be mostly consistent and reliable, not too creative"
# Think of it like: 0 = robot (same answer every time), 1 = artist (very creative)
TEMPERATURE = 0.3


# =============================================================================
# KNOWLEDGE BASE LOADER - Reading the Book Summary
# =============================================================================
def load_book_summary(file_path: str) -> str:
    """
    This function reads the parenting book summary from a file.
    
    What it does (explained like to a 5-year-old):
    Imagine you have a recipe card. This function opens that card and reads
    all the instructions so we can use them later.
    
    Parameters:
    - file_path: The location of the file (like an address: "123 Main Street")
    
    Returns:
    - The text inside the file (all the parenting advice)
    
    Example:
    If the file contains "Always acknowledge feelings", this function will
    give us that text back so our AI can use it.
    """
    try:
        # Try to open and read the file
        # 'r' means "read mode" - like opening a book to read, not write
        # 'utf-8' means the file uses standard letters and symbols
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()  # Read everything in the file
            return content  # Give back what we read
    except FileNotFoundError:
        # If the file doesn't exist, show an error message
        # This is like looking for a book that's not on the shelf
        print(f"Error: Book summary file not found at {file_path}")
        print("Please ensure book_summary.txt is in the same folder as this script.")
        return ""  # Return empty text so the program doesn't crash
    except Exception as e:
        # If something else goes wrong, show what happened
        # This catches any unexpected problems
        print(f"Error reading book summary: {str(e)}")
        return ""


# =============================================================================
# BOOK KNOWLEDGE TOOL - Making the Book Summary Searchable
# =============================================================================
class BookKnowledgeTool:
    """
    This class creates a tool that can answer questions using the book summary.
    
    Think of this like a smart bookmark that can quickly find relevant parts
    of the book when you ask a question.
    
    Example:
    You ask: "How do I handle tantrums?"
    This tool looks through the book summary and finds: "Acknowledge feelings,
    name emotions, allow space for expression"
    """
    
    def __init__(self, book_content: str):
        """
        Set up the tool with the book content.
        
        What this does:
        When we create this tool, we give it the entire book summary to remember.
        It's like giving someone a textbook and saying "memorize this for the test".
        
        Parameters:
        - book_content: All the text from the book summary file
        """
        # Store the book content so we can use it later
        # Think of this like putting the recipe in your pocket
        self.book_content = book_content
    
    def search(self, query: str) -> str:
        """
        Search the book content for relevant information.
        
        What this does (explained simply):
        When someone asks a question, this function looks through the book
        and returns the entire summary. The AI will then read through it
        to find the relevant parts.
        
        Why return everything?
        The book summary is short enough that the AI can read all of it
        quickly. This is simpler than building a complex search system.
        It's like reading a 2-page cheat sheet instead of searching a
        1000-page encyclopedia.
        
        Parameters:
        - query: The question being asked (e.g., "How to handle lying?")
        
        Returns:
        - The relevant book content (or the whole summary if it's short)
        
        Example:
        Input: "My child won't cooperate"
        Output: The entire book summary, which includes Chapter 2 about
                "Engaging Cooperation"
        """
        if not self.book_content:
            # If the book is empty, we can't help
            return "Book summary not loaded. Cannot provide guidance."
        
        # Return the entire book summary wrapped in a clear format
        # The triple quotes create a multi-line string
        return f"""
Parenting Guidance from "How to Talk So Little Kids Will Listen":

{self.book_content}

This guidance addresses common parenting situations using research-backed
communication techniques. Apply these principles to your specific situation.
"""


# =============================================================================
# INITIALIZE LLM - Setting Up the AI Brain
# =============================================================================
def initialize_llm() -> Ollama:
    """
    Create and configure the AI language model.
    
    What this does (simple explanation):
    This connects to the qwen3 AI model running on your computer. Think of it
    like turning on a very smart calculator that can understand and answer
    questions in human language.
    
    Returns:
    - A configured Ollama model ready to answer questions
    
    Important settings explained:
    - model: Which AI brain to use (qwen2.5:3b - a small but smart model)
    - temperature: How creative vs. consistent (0.3 = mostly consistent)
    - num_ctx: How much text it can remember at once (4096 words is plenty)
    
    Example:
    This is like opening a textbook and getting ready to study. The AI is
    now ready to read our questions and the book summary.
    """
    llm = Ollama(
        model=MODEL_NAME,  # Use the qwen2.5:3b model
        temperature=TEMPERATURE,  # Control creativity level
        num_ctx=4096  # How many words it can process at once (context window)
    )
    return llm


# =============================================================================
# CREATE TOOLS - Building the Agent's Abilities
# =============================================================================
def create_tools(book_content: str) -> List[Tool]:
    """
    Create the tools that the agent can use to answer questions.
    
    What this does (explained simply):
    This gives our AI agent two special abilities:
    1. Read the parenting book summary
    2. Search the internet
    
    Think of it like giving a student two resources: a textbook and access
    to Google. They can use either one depending on what helps most.
    
    Parameters:
    - book_content: The text from the book summary file
    
    Returns:
    - A list of tools the agent can use
    
    Example usage by the agent:
    Question: "My 4-year-old won't share toys"
    Agent thinks: "Let me check the book first" → Uses book_knowledge tool
    Agent thinks: "I need recent research too" → Uses web_search tool
    """
    
    # Create the book knowledge tool
    # This is Tool #1: The parenting book expert
    book_tool_instance = BookKnowledgeTool(book_content)
    book_tool = Tool(
        name="book_knowledge",  # Name the agent will use to call this tool
        description="""Use this tool FIRST for parenting questions. Contains expert advice 
        from 'How to Talk So Little Kids Will Listen' covering: handling emotions, 
        cooperation, conflict resolution, lying, tantrums, cleanup, shyness, safety, 
        and general parent-child communication. This should be your primary source.""",
        func=book_tool_instance.search  # The function to run when tool is used
    )
    
    # Create the web search tool
    # This is Tool #2: The internet search expert
    search = DuckDuckGoSearchRun()
    search_tool = Tool(
        name="web_search",  # Name the agent will use to call this tool
        description="""Use this tool for current information, recent research, or 
        specific situations not covered in the book. Search for: latest parenting 
        research, age-specific advice, medical concerns, or specialized topics. 
        Use AFTER checking book_knowledge.""",
        func=search.run  # The function to run when tool is used
    )
    
    # Return both tools in a list
    # The agent will choose which one(s) to use based on the question
    return [book_tool, search_tool]


# =============================================================================
# AGENT PROMPT TEMPLATE - Instructions for the AI
# =============================================================================
# This is the "instruction manual" we give to the AI agent
# It tells the AI HOW to think and respond

AGENT_PROMPT = """You are a compassionate parenting advisor specializing in positive 
communication with young children (ages 2-7). Your expertise comes from "How to Talk 
So Little Kids Will Listen" and current parenting research.

AVAILABLE TOOLS:
{tools}

TOOL NAMES: {tool_names}

DECISION PROCESS:
1. For general parenting questions: Use book_knowledge FIRST
2. For current events/medical/specialized topics: Add web_search
3. Always synthesize information from both sources when available

RESPONSE STYLE:
- Be warm, supportive, and non-judgmental
- Provide actionable, specific advice
- Use examples when helpful
- Acknowledge that every child and situation is different
- Keep responses practical and concise

CORE PRINCIPLES TO EMPHASIZE:
- Feelings come first, behavior comes second
- Offer choices to increase cooperation
- Use playfulness over lecturing
- Problem-solve together with the child
- Keep language simple and clear

Answer the user's question using this format:

Question: {input}

Thought: [Your reasoning about which tool to use and why]
Action: [The tool to use - either book_knowledge or web_search]
Action Input: [What to search for]
Observation: [The result from the tool]
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now have enough information to provide a helpful answer
Final Answer: [Your comprehensive, practical advice for the parent]

{agent_scratchpad}
"""


# =============================================================================
# CREATE AGENT - Assembling All the Pieces
# =============================================================================
def create_parenting_agent(llm: Ollama, tools: List[Tool]) -> AgentExecutor:
    """
    Assemble the complete AI parenting agent.
    
    What this does (simple explanation):
    This puts together all our pieces like building with LEGO blocks:
    - The AI brain (llm)
    - The tools (book knowledge + web search)
    - The instructions (prompt template)
    - The memory (to remember conversation)
    
    The result is a complete agent that can have conversations and give advice.
    
    Parameters:
    - llm: The AI language model (the brain)
    - tools: The abilities (book knowledge and web search)
    
    Returns:
    - A complete, ready-to-use agent
    
    Example:
    This is like assembling a robot. We attach the brain, give it tools
    (hands), instructions (programming), and memory. Now it's ready to work!
    """
    
    # Create the prompt template from our instructions
    # This turns our text instructions into a format the AI understands
    prompt = PromptTemplate(
        template=AGENT_PROMPT,  # Our instruction text from above
        input_variables=["input", "agent_scratchpad", "tools", "tool_names"]
        # These are placeholders that will be filled in with actual values
    )
    
    # Create the agent with ReAct (Reasoning + Acting) architecture
    # ReAct means: Think about what to do → Do it → Think about result → Repeat
    # This is how humans solve problems: think, act, observe, think again
    agent = create_react_agent(
        llm=llm,  # The AI brain
        tools=tools,  # The abilities
        prompt=prompt  # The instructions
    )
    
    # Create the executor (the manager that runs the agent)
    # The executor handles the conversation flow and tool usage
    agent_executor = AgentExecutor(
        agent=agent,  # Our configured agent
        tools=tools,  # The tools it can use
        verbose=True,  # Print what it's thinking (helpful for debugging)
        handle_parsing_errors=True,  # Don't crash if there's a small error
        max_iterations=5  # Maximum steps before giving up (prevents infinite loops)
    )
    
    return agent_executor


# =============================================================================
# MAIN EXECUTION - Starting the Agent
# =============================================================================
def main():
    """
    Main function that runs when you start the program.
    
    What this does (simple explanation):
    This is the "start button" of our program. It:
    1. Loads the parenting book
    2. Sets up the AI brain
    3. Creates the tools
    4. Builds the agent
    5. Starts the conversation loop
    
    Think of it like starting a car: turn the key (main function),
    engine starts (load book and AI), and you're ready to drive (chat).
    """
    
    print("=" * 70)
    print("AI PARENTING AGENT - Powered by 'How to Talk So Little Kids Will Listen'")
    print("=" * 70)
    print()
    
    # Step 1: Load the book summary
    # This reads the file containing all the parenting advice
    print("Loading parenting knowledge base...")
    book_content = load_book_summary(BOOK_SUMMARY_PATH)
    
    if not book_content:
        # If the book didn't load, we can't continue
        print("Failed to load book summary. Please check the file and try again.")
        return  # Exit the program
    
    print(f"Loaded {len(book_content)} characters of parenting guidance.")
    print()
    
    # Step 2: Initialize the AI model
    # This connects to qwen3 on your computer
    print("Initializing AI model (${MODEL_NAME})...")
    llm = initialize_llm()
    print("AI model ready.")
    print()
    
    # Step 3: Create the tools
    # This gives the agent its abilities (book knowledge + web search)
    print("Creating agent tools...")
    tools = create_tools(book_content)
    print(f"Created {len(tools)} tools: {[tool.name for tool in tools]}")
    print()
    
    # Step 4: Create the agent
    # This assembles everything into a working agent
    print("Assembling parenting agent...")
    agent = create_parenting_agent(llm, tools)
    print("Agent ready.")
    print()
    
    # Step 5: Start the conversation loop
    # This is where the magic happens - you can ask questions
    print("=" * 70)
    print("You can now ask parenting questions.")
    print("Type 'quit', 'exit', or 'bye' to end the conversation.")
    print("=" * 70)
    print()
    
    # Keep looping until the user wants to quit
    while True:
        # Get input from the user
        # input() waits for the user to type something and press Enter
        user_input = input("You: ").strip()
        
        # Check if user wants to quit
        # .lower() makes it not case-sensitive (QUIT = quit = Quit)
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("\nThank you for using the AI Parenting Agent. Good luck!")
            break  # Exit the loop and end the program
        
        # Skip empty inputs
        if not user_input:
            continue  # Go back to the start of the loop
        
        print()  # Empty line for formatting
        
        try:
            # Run the agent with the user's question
            # This is where the AI thinks, uses tools, and generates an answer
            response = agent.invoke({"input": user_input})
            
            # Print the final answer
            # response["output"] contains the agent's final answer
            print("\n" + "=" * 70)
            print("ADVICE:")
            print("=" * 70)
            print(response["output"])
            print("=" * 70)
            print()
            
        except KeyboardInterrupt:
            # If user presses Ctrl+C, exit gracefully
            print("\n\nInterrupted by user. Exiting...")
            break
        except Exception as e:
            # If something goes wrong, show the error but keep running
            print(f"\nError processing your question: {str(e)}")
            print("Please try rephrasing your question or check the Ollama service.")
            print()


# =============================================================================
# PROGRAM ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    """
    This special block runs when you execute this file directly.
    
    What this means (simple explanation):
    When you run this file with "python parenting_agent.py", Python checks
    if this is the main file being run. If yes, it runs main().
    
    Think of it like this: if this recipe book is the one you're cooking from
    (not just referenced by another recipe), then start cooking!
    """
    main()