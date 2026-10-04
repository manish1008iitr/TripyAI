import sys
from pathlib import Path
import os 
import asyncio
# from  langchain_mcp_adapters.client import MultiServerMCPClient


# Import dotenv to load environment variables from .env file
import dotenv
dotenv.load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


from langchain.mcp import MCPAdapter
from fastmcp import ClientGroup, Client
from fastmcp.client.transports import StdioTransport, StreamableHttpTransport


weather_info = StdioTransport(
    command="python",
    args=[r"C:\Users\ranju\OneDrive\Documents\Code_Projects\TripyAI\mcp_servers\weather_mcp_server.py"]
)


flight_info = StdioTransport(
    command="python",
    args=[r"C:\Users\ranju\OneDrive\Documents\Code_Projects\TripyAI\mcp_servers\flight_mcp_server.py"]
)

tavily_client = StreamableHttpTransport(
    url=f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
)



async def get_tavily_tools():
    async with MCPAdapter(tavily_client) as adapter:
        tools = await adapter.list_tools()
    return tools

async def flight_info_tools():
    async with MCPAdapter(weather_info) as adapter:
        tools = await adapter.list_tools()
    return tools 

async def weather_info_tools():
    async with MCPAdapter(flight_info) as adapter:
        tools = await adapter.list_tools()
    return tools





# ***************************************************************************************
#                    PRACTICE CODE
# ****************************************************************************************


# if __name__ == "__main__":
#     weather_tools = asyncio.run(weather_info_tools())
#     weather_tools.extend(asyncio.run(flight_info_tools()))
#     tavily_tools = asyncio.run(get_tavily_tools())
#     for tool in tavily_tools:
#         print("Weather Tools:", tool.name)

    
#     for tool in weather_tools:
#         print("Weather Tools:", tool.name)


# AVIATION_STACK_API_KEY = os.getenv("AVIATION_STACK_API_KEY")
# OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
# print("TAVILY_API_KEY:", TAVILY_API_KEY)
# print("AVIATION_STACK_API_KEY:", AVIATION_STACK_API_KEY)

# multi_server_config = ClientGroup({
#         "tavily_search": Client(),
#         "weather_info": Client(weather_info),
#         "flight_info":Client(flight_info)
#     })
