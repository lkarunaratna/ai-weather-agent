"""Tool implementations for the weather_agent package.

Author: Lakshitha Karunaratna
Created: 2026-02-09

This module contains Python functions that fetch external data.
"""
from typing import Dict
import requests


def get_weather(city: str) -> str:
    """Fetch current weather for `city` using the free wttr.in API.

    Returns a short string. This function catches errors and
    returns an error message instead of raising so the caller 
    can handle failures gracefully.
    """
    try:
        resp = requests.get(f"https://wttr.in/{city}?format=j1", timeout=10)
        if resp.status_code != 200:
            return f"Could not fetch weather for {city} (HTTP {resp.status_code})"

        data = resp.json()
        current = data["current_condition"][0]
        temp_c = current.get("temp_C")
        desc = current.get("weatherDesc", [{}])[0].get("value")
        return f"Weather in {city}: {desc}, Temperature: {temp_c}°C"
    except Exception as e:
        return f"Error fetching weather: {e}"


# Adapter for LangChain tools: a mapping to match what the LLM returns.

def execute_tool(call: Dict) -> str:
    """Execute a tool call dict and return the result string.

    Expected `call` shape: {"name": "get_weather", "args": {"city": "..."}}
    """
    name = call.get("name")
    args = call.get("args") or {}

    if name == "get_weather":
        return get_weather(args.get("city") or "")

    return f"Unknown tool: {name}"
