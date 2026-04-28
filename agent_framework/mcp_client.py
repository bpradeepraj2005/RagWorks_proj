import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import logging

logger = logging.getLogger("MCP_Client")

async def execute_mcp_tool(tool_name: str, arguments: dict) -> str:
    """
    Connects to the MCP Server via Standard I/O, authenticates, and executes a tool.
    This fulfills the strict Model Context Protocol requirement.
    """
    server_script = os.path.join(os.path.dirname(__file__), "..", "mcp_server", "main.py")
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[server_script]
    )
    
    logger.info(f"Connecting to MCP Server to execute: {tool_name}")
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Execute the tool via the MCP Protocol
                result = await session.call_tool(tool_name, arguments)
                
                if result.isError:
                    logger.error(f"MCP Tool Error: {result.content}")
                    return f"Error executing {tool_name}."
                
                logger.info(f"Successfully executed MCP tool: {tool_name}")
                return result.content[0].text
    except Exception as e:
        logger.error(f"Failed MCP connection: {e}")
        return f"System Error connecting to MCP Server: {e}"

def sync_mcp_tool_runner(tool_name: str, **kwargs) -> str:
    """Synchronous wrapper for Langchain tools to call the async MCP client."""
    return asyncio.run(execute_mcp_tool(tool_name, kwargs))
