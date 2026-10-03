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

llm = ChatGroq(
    model= os.getenv("MODEL_NAME"),
    api_key= CHATGROQ_API_KEY,
    temperature=0,  # Keeping temperature at 0 ensures higher determinism for data extraction
    model_kwargs={
        "tool_choice": "auto"  # or "required", or a specific tool definition
    }
)


async def main():
    client = MultiServerMCPClient(Server)
    tools = await client.get_tools()
    print("Available tools:", [tool.name for tool in tools])
    tavely_search_tool = next(tool for tool in tools if tool.name == "tavily_search")   

    # Alternatively, use a LangChain/LangGraph agent which handles tool execution loop
    # agent = create_agent(llm, tools)
    result = await tavely_search_tool.ainvoke({"query":"Tell me latest news about AI"})
    print(result)


    # llm_with_tool = llm.bind_tools([tavely_search_tool])
    # response = await llm_with_tool.ainvoke("Tell me latest news about AI")
    # print(response.content)

if __name__ == "__main__":
    asyncio.run(main())





