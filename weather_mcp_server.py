import os 
import requests
from fastmcp import FastMCP
# load the environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

OPEN_WEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

mcp = FastMCP("Weather MCP Server")

@mcp.tool(description="Fetches weather information for a given city.")
def get_current_city_weather(city: str) -> str:
    response = requests.get(
        "http://api.openweathermap.org/data/2.5/weather",
        params = {
            "q":city,
            "appid":OPEN_WEATHER_API_KEY,
            "units":"metric"
        })
    #Handling responses
    if response.status_code != 200:
        return f"Error fetching weather data: {response.status_code} - {response.text}"

    data = {
        "city":city,
        "temperature_city": response["main"]["temp"],
        "feels_like_city": response["main"]["feels_like"],
        "humidity": response["main"]["humidity"],
        "weather_description": response["weather"][0]["description"],
        "wind_speed": response["wind"]["speed"]
    }

    return data
    


@mcp.tool(description="Fetches weather forecast for a given city.")
def get_weather_forecast_city(city: str) -> str:
    response = requests.get(
        "http://api.openweathermap.org/data/2.5/forecast", 
        params = {
            "q":city,
            "appid":OPEN_WEATHER_API_KEY,
            "units":"metric"
        })

    if response.status_code != 200:
        return f"Error fetching weather forecast data: {response.status_code} - {response.text}"

    data = response.json()
    forecast = []

    # Return first 5 forecast entries
    for item in data["list"][:5]:
        forecast.append(
            {
                "datetime": item["dt_txt"],
                "temperature": item["main"]["temp"],
                "weather": item["weather"][0]["description"]
            }
        )

    data =  {
        "city": city,
        "forecast": forecast
    }

    return data

if __name__ == "__main__":
    mcp.run()