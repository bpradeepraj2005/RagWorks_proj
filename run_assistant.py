import os
import sys
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    print("Warning: GROQ_API_KEY is not set in your .env file!")
    print("The agent will crash if it tries to route questions without it.\n")

from agent_framework.multi_agent import run_agent_system

print("===============================================")
print("🤖 AI Shopping Assistant 🤖")
print("===============================================")
print("Ask about products, policies, or manage your cart.")
print("Type 'exit' or 'quit' to close.")
print("-----------------------------------------------")

def chat_loop():
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit", "q"]:
                break
                
            print("\n🤖 Processing...")
            response = run_agent_system(user_input)
            print(f"\nAssistant: {response}")
            print("-" * 50)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    chat_loop()
