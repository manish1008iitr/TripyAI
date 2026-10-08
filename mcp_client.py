import asyncio
import os
from langchain.mcp import MCPAdapter
from fastmcp import ClientGroup, Client
from fastmcp.client.transports import StdioTransport, StreamableHttpTransport



# Import dotenv to load environment variables from .env file
import dotenv
dotenv.load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


from langchain_groq import ChatGroq
from langchain.agents import create_agent


llm = ChatGroq(
    model= os.getenv("MODEL_NAME"),
    api_key= os.getenv("GROQ_API_KEY"),
    temperature=0,  # Keeping temperature at 0 ensures higher determinism for data extraction
    model_kwargs={
        "tool_choice": "auto"  # or "required", or a specific tool definition
    }
)

#Creating Weather Info transfer object 
weather_info = StdioTransport(
    command="python",
    args=[r"C:\Users\ranju\OneDrive\Documents\Code_Projects\TripyAI\mcp_servers\weather_mcp_server.py"]
)

#Creating Flight Info transfer object 
flight_info = StdioTransport(
    command="python",
    args=[r"C:\Users\ranju\OneDrive\Documents\Code_Projects\TripyAI\mcp_servers\flight_mcp_server.py"]
)

#Creating Tavily Search Info transfer object 
tavily_client = StreamableHttpTransport(
    url=f"https://mcp.tavily.com/mcp/?tavilyApiKey={TAVILY_API_KEY}"
)

#Function to fetch Tavily tools
async def get_tavily_tools():
    async with MCPAdapter(tavily_client) as adapter:
        tools = await adapter.list_tools()
        return tools

#Functions to fetch flight information search tools from a local MCP server
async def get_flight_info_tools(query):
    async with MCPAdapter(flight_info) as adapter:
        tools = await adapter.list_tools()
        system_message = """
                    You are a helpful AI assistant.
            
                    Your job is to answer the user's questions accurately.
            
                    You have access to several tools.
            
                    Rules:
                    1. Decide yourself which tool is appropriate for the user's question.
                    2. Only use a tool when it is necessary.
                    3. You may use multiple tools if the question requires them.
                    5. After using a tool, explain the result clearly to the user.
                    6. Never invent tool results.
                """
        
            # print("LLM response:")
        
        agent = create_agent(
                model = llm, 
                tools = tools, 
                system_prompt= system_message
            )
        
        
        result = await agent.ainvoke({
                "messages": [
                    {
                        "role": "user",
                        "content": query
                    }
                ]
            })
        
    return result["messages"][-1].content

#Functions to Weather information search tools from a local MCP server
async def get_weather_info_tools():
    async with MCPAdapter(weather_info) as adapter:
        tools = await adapter.list_tools()
    return tools


# ***************************************************************************************
#                                 PRACTICE CODE
# ****************************************************************************************


async def flight_agent():
    print("function reached till here")
    result = await get_flight_info_tools()
    print(result)
    # tools = await get_flight_info_tools()

    # system_message = """
    #         You are a helpful AI assistant.
    
    #         Your job is to answer the user's questions accurately.
    
    #         You have access to several tools.
    
    #         Rules:
    #         1. Decide yourself which tool is appropriate for the user's question.
    #         2. Only use a tool when it is necessary.
    #         3. You may use multiple tools if the question requires them.
    #         5. After using a tool, explain the result clearly to the user.
    #         6. Never invent tool results.
    #     """

    # # print("LLM response:")

    # agent = create_agent(
    #         model = llm, 
    #         tools = tools, 
    #         system_prompt= system_message
    #     )


    # result = await agent.ainvoke({
    #        "messages": [
    #            {
    #                "role": "user",
    #                "content": "get me flight from delhi to tokyo"
    #            }
    #        ]
    #    })

    # print(result["messages"][-1].content)
    
    # return {
    #     "flight_results":result["messages"][-1].content, 
    #     "messages": AIMessage(content="Hotel information fetched.")
    #     }






if __name__ == "__main__":
    asyncio.run(flight_agent())
    # weather_tools = asyncio.run(get_weather_info_tools())
    # weather_tools.extend(asyncio.run(get_flight_info_tools()))
    # tavily_tools = asyncio.run(get_tavily_tools())
    # for tool in weather_tools:
    #     print("Flight tools:", tool.name)

    
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

   # print(result)

    # print("Tool calls:")
    # print(result.tool_calls)

    # # Get the first tool call
    # tool_call = result.tool_calls[0]

    # tool_name = tool_call["name"]
    # tool_args = tool_call["args"]

    # print("Tool name:", tool_name)
    # print("Tool args:", tool_args)

    # # Find the actual tool object
    # selected_tool = next(
    #     tool for tool in tools
    #     if tool.name == tool_name
    # )

    # # Invoke the actual tool asynchronously
    # tool_result = await selected_tool.ainvoke(tool_args)

    # print("Tool result:")
    # print(tool_result)