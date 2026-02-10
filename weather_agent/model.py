"""Model and orchestration helpers for weather_agent.

Author: Lakshitha Karunaratna
Created: 2026-02-09

This module contains functions to create the Chat model, bind tools, and run
queries. The functions are intentionally small and documented for beginners.
"""
import os
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


def create_model(api_key: str | None = None, model_name: str = "gpt-4.1-nano", temperature: float = 0):
    """Create and return a ChatOpenAI model instance.

    - `api_key`: if None, it will be read from the `OPENAI_API_KEY` environment
      variable.
    - `model_name`: the LLM identifier.
    - `temperature`: randomness control (0 = deterministic).
    """
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")

    model = ChatOpenAI(model=model_name, temperature=temperature, api_key=api_key)
    return model


def build_messages(user_text: str) -> List[HumanMessage]:
    """Helper to build a minimal conversation payload for the model."""
    return [HumanMessage(content=user_text)]
