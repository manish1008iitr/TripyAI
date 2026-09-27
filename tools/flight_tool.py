from __future__ import annotations
import os

from typing import Any
import re
import airportsdata
import pycountry
from dotenv import load_dotenv
import requests
load_dotenv()

AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
DEFAULT_ORIGIN_IATA = os.getenv("DEFAULT_ORIGIN_IATA")
AVIATIONSTACK_URL = "https://api.aviationstack.com/v1/flights"

REQUEST_TIMEOUT = 15

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
    class find_dest_board(BaseModel):
        departure_code:str = Field(description = "boarding aiport code mention in the quesry")
        destination_code:str = Field(description= "destination aiport code mention in the query")
        summary:str = Field(description="when you dont able to find a suitable airport")

    ## STRCUTURED LLM CREATION
    structured_llm = llm.with_structured_output(find_dest_board, method="json_schema")

    # Creating prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert in finding boarding and destination airport code from user query"
        "You are supposed to find a suitable airport in nearby based on boarding place and destination place"
        "If you dont able to find a suitable aiport simply answer please mention particular place"
        "Answer only in term of destination and boarding airport code"),
        ("human", "{query}")
    ])

    chain = prompt | structured_llm
    result = chain.invoke({"query": query})

    departure_code = result.departure_code
    destination_code = result.destination_code
    summary = result.summary

    return {"departure_code":departure_code,
        "destination_code": destination_code,
        "summary":summary}

def search_flights(departure_iata, destination_iata):
    params = {
        'access_key': AVIATIONSTACK_API_KEY,
        'dep_iata': departure_iata.upper(),  # Boarding airport code
        'arr_iata': destination_iata.upper(),  # Destination airport code
        'limit': 20                              # Number of results to return
    }
    response = requests.get(AVIATIONSTACK_URL, params=params).json()
    flights = response.get('data', [])
    if not flights:
        return "No flight is found between them"
    else:
        return flights

def final_flight_result(query):
    response = search_codes(query)
    if response["departure_code"] and response["destination_code"]:
        flights = search_flights(response["departure_code"], response["destination_code"])
    else:
        flights = response["summary"]
    return flights

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


    

