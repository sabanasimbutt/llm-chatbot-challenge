# Generative AI Chatbot for Customer Service

---

## 1. Project Overview

The task is to design and build a fully generative chatbot that uses a Large Language Model (LLM) to handle customer service requests while adhering to specific company policies. The chatbot is designed to integrate with backend APIs for actions like order tracking and cancellation.

The core of this solution is an **LLM-powered agent** that can reason about a user's request, decide which tool to use, execute it, and then formulate a helpful, context-aware response. This implementation also includes conversational memory, allowing the chatbot to remember context from previous turns in the conversation.

---

## 2. Solution Architecture: The ReAct Framework

To build a reliable and auditable system, I chose an architecture based on the **ReAct (Reasoning and Acting)** framework. This approach separates the LLM's roles, making the system more robust and preventing the model from "hallucinating" actions that violate business rules.

The conversation flow follows these distinct steps:

1.  **Reason (Thought):** The LLM first analyzes the user's query and the conversation history to form a "thought." It determines the user's intent and decides which tool (e.g., `OrderCancellation`) is needed and what parameters (e.g., `orderId`) are required.
2.  **Act (Tool Use):** The system's backend code executes the chosen tool. **Crucially, all business logic and policies (like the 10-day cancellation window) are enforced within these tools, not by the LLM.** This ensures that company policies are always followed.
3.  **Observe (Tool Result):** The result from the tool (e.g., `{"success": false, "reason": "Order is too old."}`) is passed back to the system.
4.  **Generate Final Response:** The LLM receives the tool's result and its final task is to translate that structured data into a friendly, human-readable response for the user.

This decoupled architecture is a key design choice. It leverages the LLM for its powerful natural language understanding and generation capabilities while keeping critical business logic in secure, deterministic code.

---

## 3. How to Run the Project

This project is structured as a Python application with a clear separation between the agent logic and the API tools.

### Prerequisites

* Python 3.7+
* A virtual environment tool (like `venv`)

### Setup

1.  **Clone the repository:**
    ```bash
    git clone <repo-url>
    cd <repo-directory>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # Create the environment
    python -m venv venv

    # Activate it (macOS/Linux)
    source venv/bin/activate
    
    # Or activate it (Windows)
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    The `requirements.txt` file contains all necessary packages.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API Key:**
    Create a file named `.env` in the root of the project directory. Inside this file, add your Gemini API key like so:
    ```
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```
    The `chatbot_agent.py` script will automatically load this key.

### Running the Chatbot

To start the interactive chat session, run the `chatbot_agent.py` script from your terminal:

```bash
python chatbot_agent.py