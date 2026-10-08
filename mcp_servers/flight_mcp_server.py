from __future__ import annotations
import os

from typing import Any
import requests


#To load environment variables
from dotenv import load_dotenv
load_dotenv()


#TO make a local MCP server 
from fastmcp import FastMCP
mcp = FastMCP("Flight Search Tool")

AVIATION_STACK_API_KEY = os.getenv("AVIATION_STACK_API_KEY")
DEFAULT_ORIGIN_IATA = os.getenv("DEFAULT_ORIGIN_IATA")
AVIATIONSTACK_URL = "https://api.aviationstack.com/v1/flights"



from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import  BaseModel, Field
load_dotenv()

#LLM CREATION
llm = ChatGroq(
    model=os.getenv("MODEL_NAME"),
    api_key= os.getenv("GROQ_API_KEY"),
    temperature=0,  # Keeping temperature at 0 ensures higher determinism for data extraction
    model_kwargs = {
        "tool_choice": "auto"  # or "required", or a specific tool definition
    }
)


def search_codes(query):
    """Get airport codes codes of the  source and destination major airports"""
    class find_aiport_codes(BaseModel):
        departure_code:str = Field(description = "boarding aiport code mention in the quesry")
        destination_code:str = Field(description= "destination aiport code mention in the query")

    ## STRCUTURED LLM CREATION
    structured_llm = llm.with_structured_output(find_aiport_codes, method="json_schema")

    # Creating prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in finding boarding and destination airport code from user query"

        "Important instruction to follow"
            "Find a suitable airport in nearby based on boarding place and destination place"
            "Answer only in term of destination and boarding airport code"),
        ("human", "{query}")
    ])

    chain = prompt | structured_llm
    result = chain.invoke({"query": query})

    departure_code = result.departure_code
    destination_code = result.destination_code

    return {
        "departure_code":departure_code,
        "destination_code": destination_code
        }

def search_flights(departure_iata, destination_iata):
    """Search flights between a source and destination."""
    params = {
        'access_key': AVIATION_STACK_API_KEY,
        'dep_iata': departure_iata.upper(),  # Boarding airport code
        'arr_iata': destination_iata.upper(),  # Destination airport code
        'limit': 8                              # Number of results to return
    }
    response = requests.get(AVIATIONSTACK_URL, params=params).json()
    flights = response.get('data', [])
    if flights:
        return flights 
    else:
        return "No flight is found between them"


@mcp.tool(description="Give result related to flight details")
async def final_flight_result(query:str):
    """Get available flights between a source and destination."""
    response = search_codes(query)
    print("Codes are ", response)
    if response["departure_code"] and response["destination_code"]:
        flights = search_flights(response["departure_code"], response["destination_code"])
    else:
        flights = response["summary"]
    return flights

if __name__ == "__main__":
    mcp.run()











    # for flight in flights:
    #     airline_name = flight['airline']['name']
    #     flight_num = flight['flight']['number']
    #     status = flight['flight_status']
    #     sched_dep = flight['departure']['scheduled']
    #     sched_arr = flight['arrival']['scheduled']
            
    #     print(f"✈️ Airline: {airline_name} | Flight: {flight_num}")
    #     print(f"   Status: {status.upper()}")
    #     print(f"   Departure: {sched_dep}")
    #     print(f"   Arrival:   {sched_arr}")
    #     print("-" * 40)


    

