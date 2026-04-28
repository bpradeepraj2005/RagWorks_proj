import os
import logging
from typing import Tuple

# Set up global observability logger
log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, 'system_trace.log'),
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
logger = logging.getLogger("Guardrails")

def input_guardrail(user_input: str) -> Tuple[bool, str]:
    """
    Validates user input. Blocks unsafe or restricted requests.
    Returns (is_safe, message_if_unsafe)
    """
    restricted_keywords = ["weapon", "gun", "drugs", "illegal", "explosive", "hack", "bypass"]
    user_input_lower = user_input.lower()
    
    for word in restricted_keywords:
        if word in user_input_lower:
            logger.warning(f"Safety constraint triggered: Restricted keyword '{word}' detected.")
            return False, f"I'm sorry, but I cannot assist with purchases or inquiries related to restricted items."
            
    # Basic SQLi/Prompt Injection constraint
    if "drop table" in user_input_lower or "system prompt" in user_input_lower:
        logger.warning("Safety constraint triggered: Potential Injection attempt.")
        return False, "Invalid input structure detected."

    return True, ""
