# chatbot_agent.py
# Main application file for the generative AI chatbot.

import json
import requests
import re
import ast
import os

from dotenv import load_dotenv
load_dotenv()

# Import the tools from our separate backend file
from api_tools import OrderTracking, OrderCancellation

# --- Tool Registry ---
# The agent uses this to know what functions are available.
available_tools = {
    "OrderTracking": OrderTracking,
    "OrderCancellation": OrderCancellation,
}

# --- LLM Interaction & Prompting ---
import google.generativeai as genai
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

def call_gemini_api(prompt: str, is_json: bool = False) -> str:
    try:
        model_gemini = genai.GenerativeModel('gemini-2.5-flash')
        response = model_gemini.generate_content(prompt)
        output = response.text
        return output
    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Error parsing Gemini API response: {e}\nFull response: {response.text}")
        return None

def get_llm_action_plan(user_query: str, chat_history: list) -> dict:
    """
    Generates the first prompt to get a structured action plan from the LLM, with conversation history for context.
    """
    # Format the chat history for inclusion in the prompt
    formatted_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])

    prompt = f"""
    You are a helpful and polite customer service chatbot. Your goal is to assist users with their orders by using the tools available to you.
    You have the context of the current conversation. Use it to inform your decisions, such as remembering an order ID a user has already provided.

    ## Conversation History:
    {formatted_history}

    ## Available Tools:
    You have access to the following tools. Use them when necessary.

    - `OrderTracking`: Use this to get the status of an order.
      - Parameters: `{{ "orderId": "string" }}`

    - `OrderCancellation`: Use this to cancel an order.
      - Parameters: `{{ "orderId": "string" }}`

    ## Company Policies & Your Rules:
    1.  **Order Cancellation Policy**: You MUST use the `OrderCancellation` tool to check eligibility. The tool enforces the 10-day policy.
    2.  **Use Conversation History**: If the user has already provided an order ID in a previous message, use it. Do not ask for it again.
    3.  **Ask for Missing Information**: If you need an `orderId` and it's not in the history or the current query, you MUST ask for it.

    ## Your Task:
    Based on the user's latest request and the conversation history, respond with a JSON object:
    {{
      "thought": "Your step-by-step reasoning. Mention if you are using information from the chat history.",
      "tool_to_use": "The name of the tool to use (e.g., 'OrderTracking', 'OrderCancellation', or 'none').",
      "parameters": {{}},
      "response_to_user": "A message to the user ONLY if you need more information. Otherwise, an empty string."
    }}

    ## User's Latest Request:
    "{user_query}"

    Your JSON response:
    """
    response_text = call_gemini_api(prompt, is_json=True)
    if response_text:
        try:
            match = re.search(r"\{.*\}", response_text, re.DOTALL)
            response_text = ast.literal_eval(match.group(0))
            return response_text
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from LLM response.\nRaw response: {response_text}")
            return None
    return None

def get_final_response(user_query: str, tool_result: dict) -> str:
    """
    Generates the second prompt to get a natural language response from the LLM.
    """
    prompt = f"""
    You are a customer service chatbot. A user made a request, a tool was run, and you now have the result of that action.
    Your task is to formulate a friendly, clear, and helpful response to the user based on the outcome.

    - User's Original Request: "{user_query}"
    - Tool Result: {json.dumps(tool_result, indent=2, default=str)}

    Based on this result, write a natural and helpful response.
    - If the action was successful, confirm it clearly.
    - If there was an error (e.g., order not found, policy violation), explain it politely.
    - Do not output the raw JSON from the tool result in your response.
    """
    return call_gemini_api(prompt)

# --- Agent Orchestration ---

def process_user_query(user_query: str, chat_history: list) -> str:
    """
    Orchestrates the chatbot's response and returns the final response text.
    """
    print("---------------------------------------------")
    # 1. Get action plan from LLM, now with history
    action_plan = get_llm_action_plan(user_query, chat_history)
    if not action_plan:
        final_response = "I'm sorry, I had trouble understanding that. Could you please rephrase?"
        print(f"Assistant: {final_response}")
        return final_response

    print(f"Thought Process:\n{action_plan.get('thought')}\n")
    
    tool_name = action_plan.get("tool_to_use")
    
    # 2. Execute tool or respond directly
    if tool_name and tool_name != "none":
        if tool_name in available_tools:
            tool_function = available_tools[tool_name]
            parameters = action_plan.get("parameters", {})
            tool_result = tool_function(**parameters)
            print(f"Tool Result ({tool_name}):\n{json.dumps(tool_result, indent=2, default=str)}\n")
            
            # 3. Formulate final response
            final_response = get_final_response(user_query, tool_result)
        else:
            final_response = f"I'm sorry, I tried to use a tool called '{tool_name}' but it's not available."
    else:
        final_response = action_plan.get("response_to_user", "I'm not sure how to help with that.")

    print(f"🤖 Assistant: {final_response}")
    return final_response

# --- Main Conversational Loop ---
def main():
    """
    Runs the main interactive chat session with conversation memory.
    """
    print("Generative AI Chatbot Session Started 🎉")
    print("Type 'quit' or 'exit' to end the session.")
    
    # Initialize the chat history
    chat_history = []
    
    while True:
        user_query = input("\nYou: ")
        if user_query.lower() in ["quit", "exit"]:
            print("Goodbye!")
            break
        
        # Process the query and get the bot's response
        bot_response = process_user_query(user_query, chat_history)
        
        # Update the history with the latest turn
        chat_history.append({"role": "user", "content": user_query})
        if bot_response:
            chat_history.append({"role": "assistant", "content": bot_response})

if __name__ == "__main__":
    main()
