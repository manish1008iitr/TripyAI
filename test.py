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

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,  # Keeping temperature at 0 ensures higher determinism for data extraction
    model_kwargs={
        "tool_choice": "auto"  # or "required", or a specific tool definition
    }
)

structured_llm = llm.with_structured_output(search_route, method="json_schema")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in finding boarding and destination airport from user query. "
    "Answer only in term of destination and boarding aiport codes"),
    ("human", "{query}")
])
query = "I am looking to travel from delhi to london."

chain = prompt | structured_llm

result = chain.invoke({"query": query})

print(result)

