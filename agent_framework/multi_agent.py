import os
import sys
import logging
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from agent_framework.guardrails import input_guardrail
from agent_framework.mcp_client import sync_mcp_tool_runner

# Ensure RAG Engine can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from rag_engine.vector_db import RAGEngine

logger = logging.getLogger("MultiAgentSystem")
rag = RAGEngine()

# --- RAG Tool ---
@tool
def search_store_policies(question: str) -> str:
    """Useful for answering questions about store policies, warranties, returns, and shipping."""
    logger.info(f"Support Agent querying RAG for: {question}")
    return rag.query(question)

# --- MCP Tools ---
@tool
def search_products(query: str, category: str = None) -> str:
    """Search for products across e-commerce platforms."""
    return sync_mcp_tool_runner("search_products", query=query, category=category)

@tool
def check_budget(category: str = None) -> str:
    """Check budget status."""
    return sync_mcp_tool_runner("check_budget", category=category)

@tool
def add_to_cart(product_id: str, quantity: int = 1) -> str:
    """Add item to cart and process budget constraints."""
    return sync_mcp_tool_runner("add_to_cart", product_id=product_id, quantity=quantity)

# --- LLM and Agent Setup ---
api_key = os.getenv("GROQ_API_KEY", "dummy_key_to_prevent_crash")
# Using llama-3.3-70b-versatile which is Groq's active tool-calling model
llm = ChatGroq(temperature=0, groq_api_key=api_key, model_name="llama-3.3-70b-versatile")

# Support Agent (RAG)
support_tools = [search_store_policies]
support_executor = create_react_agent(llm, tools=support_tools)

# Shopping Agent (MCP)
shopping_tools = [search_products, check_budget, add_to_cart]
shopping_executor = create_react_agent(llm, tools=shopping_tools)

def run_agent_system(user_message: str) -> str:
    logger.info(f"Received user message: {user_message}")
    
    # 1. Evaluate Guardrails
    is_safe, msg = input_guardrail(user_message)
    if not is_safe:
        return f"Safety Intervention: {msg}"
        
    # 2. Supervisor Routing Decision
    router_prompt = f"""You are a Supervisor Agent. Route the following user message to either the 'SUPPORT' agent (for policy, warranty, shipping questions) or the 'SHOPPING' agent (for buying, searching products, budgets). Reply with ONLY 'SUPPORT' or 'SHOPPING'.
    
    User Message: {user_message}"""
    
    try:
        route_decision = llm.invoke(router_prompt).content.strip().upper()
        logger.info(f"Supervisor routed request to: {route_decision}")
        
        if "SUPPORT" in route_decision:
            response = support_executor.invoke({"messages": [("user", user_message)]})
            return response['messages'][-1].content
        else:
            response = shopping_executor.invoke({"messages": [("user", user_message)]})
            return response['messages'][-1].content
            
    except Exception as e:
         logger.error(f"Agent Framework Error: {e}")
         return f"System Error: Please ensure GROQ_API_KEY is correctly set. ({e})"
