import os 
import certifi 
from  dotenv import load_dotenv
load_dotenv()

from typing import TypedDict, Annotated
import operator 
import uuid


from langgraph.graph import StateGraph, START, END
from langchain.agents import create_agent

from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)
from langchain_groq import ChatGroq
from mcp_client import get_tavily_tools, get_flight_info_tools, get_weather_info_tools


## SETTING UP THE LLM
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing. Please add it to your .env file.")

llm = ChatGroq(
    model= os.getenv("MODEL_NAME"),
    api_key= GROQ_API_KEY,
    temperature=0,  # Keeping temperature at 0 ensures higher determinism for data extraction
    model_kwargs={
        "tool_choice": "auto"  # or "required", or a specific tool definition
    }
)

class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int


#**************************************************************************
                            #Flight Agent
#***************************************************************************

async def flight_agent(state: TravelState):
    print("function reached till here")
    result = await get_flight_info_tools(state["user_query"])
    print(result)
    
def hotel_agent(state: TravelState):
    pass
#     query = f"Best hotels for {state['user_query']}"
#     hotel_results = get_tavily_result(query)

#     prompt = f"""
#             You are a great summarizer and knows vey well how to summarize a text which can be displayed in webpage
#             Remove unnecessary words and summarize the text without deleting important details.
#             Dont suggest road trip or rail trip. 
#             Try to remain concise and asnwer within 200 words only
#             Also give a heading at above in larger font like "Hotel Suggestions" with a underline
#             The text is here {hotel_results}
#         """

#     response = llm.invoke([
#         SystemMessage(content="You are an expert travel planner"),
#         HumanMessage(content=prompt)
#     ])

#     return {
#         "hotel_results": response.content,
#         "messages": [
#             AIMessage(content="Hotel information fetched.")
#         ]
#     }

def itinerary_agent(state: TravelState):
    pass
#     prompt = f"""
# Create a complete travel itinerary.

# User Query:
# {state['user_query']}

# Flight Results:
# {state['flight_results']}

# Hotel Results:
# {state['hotel_results']}

# Suggest local best food place and traditional local items that can be explored
# Make the itinerary practical, budget-aware, and easy to follow.
# Answer only in 150 words without removing important details
# Also give a heading at above in larger font like "Itinerary Plan" with a underline
# """

#     response = llm.invoke([
#         SystemMessage(content="You are an expert travel planner."),
#         HumanMessage(content=prompt)
#     ])

#     return {
#         "itinerary": response.content,
#         "messages": [response]
#     }




def final_agent(state: TravelState):
    pass
#     final_prompt = f"""
# Generate the final travel response for the user.

# User Request:
# {state['user_query']}

# Flights:
# {state['flight_results']}

# Hotels:
# {state['hotel_results']}

# Itinerary:
# {state['itinerary']}

# Format the final answer beautifully using these sections:

# 1. Trip Summary
# 2. Flight Information
# 3. Hotel Suggestions
# 4. Day-by-Day Itinerary
# 5. Estimated Budget
# 6. Final Recommendations

# Important:
# - Be clear and practical.
# - Mention that live flight API may not provide ticket prices if pricing is unavailable.
# - Keep the response useful for real travel planning.
# """

#     response = llm.invoke([
#         SystemMessage(content="You are a professional AI travel booking assistant."),
#         HumanMessage(content=final_prompt)
#     ])

#     return {
#         "messages": [response]
#     }


#*********** GRAPH ADDITION **********



graph = StateGraph(TravelState)

graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("itinerary_agent", itinerary_agent)
graph.add_node("final_agent", final_agent)

#creating nodes 

graph.add_edge(START, "flight_agent")
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "itinerary_agent")
graph.add_edge("itinerary_agent", "final_agent")
graph.add_edge("final_agent", END)


travel_graph = graph.compile()


async def run_travel_agent(user_input: str, thread_id: str | None = None):
    print("query reached run travel agent")
    if not thread_id:
        thread_id = f"user_{uuid.uuid4().hex}"

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    state_params: TravelState = {
            "messages": [
                HumanMessage(content=user_input)
            ],
            "user_query": user_input,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "llm_calls": 0
    }

    result = await travel_graph.ainvoke(
        state_params,
        config=config
    )

    final_answer = result["messages"][-1].content
    print(final_answer)

    return {
        "thread_id": thread_id,
        "answer": final_answer,
        "flight_results": result.get("flight_results", ""),
        "hotel_results": result.get("hotel_results", ""),
        "itinerary": result.get("itinerary", "")
    }

