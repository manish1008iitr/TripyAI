import os 
import asyncio
from dotenv import load_dotenv
load_dotenv()

from httpx2 import query
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langchain.agents import create_agent

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
CHATGROQ_API_KEY = os.getenv("CHATGROQ_API_KEY")

Server = {
    "tavily_search": {
        "transport": "streamable_http",
        "url": f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}",
    },
}

async def get_tavily_search_tool():
    client = MultiServerMCPClient(Server)
    tools = await client.get_tools()
    tavely_search_tool = next(tool for tool in tools if tool.name == "tavily_search")   

async def get_tavily_result(query: str) -> str:
    tavely_search_tool = await get_tavily_search_tool()

    #lets invoke the tavely search tool with a query
    result = await tavely_search_tool.invoke({
        "query":query
    })
    return result 






