from tools.tavily_tool import tavily_search

# res = tavily_search("Best hotels in india")
# print(res)

from typing import TypedDict
from pydantic import BaseModel, Field
class search_route(BaseModel):
    destination:str 
    beginning:str

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


user_input = input("enter here \n")
from backend import run_travel_agent
response = run_travel_agent(user_input, "test_user")
print("\n", response["answer"])
