from fastapi import FastAPI
from pydantic import BaseModel
from backend import run_travel_agent
import json

#Nested events lops
import nest_asyncio
nest_asyncio.apply()

app = FastAPI()

class TripRequest(BaseModel):
    query:str

@app.get("/")
def root():
    return {
        "message":"app is runnning now"
    }

@app.post("/trip-plan")
async def trip_plan(request: TripRequest):
    query = request.query
    print("query recieved")
    result = run_travel_agent(query,"test_user")
    for i in result["flight_results"]:
        print(i)
    # print(result["flight_results"])
    # result = json.loads(result)
    return result

@app.get("/health")
async def health_check():
    return "the app is working well"