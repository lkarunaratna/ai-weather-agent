"""Command-line runner for the weather_agent package.

Author: Lakshitha Karunaratna
Created: 2026-02-09

This module shows how to wire the model and tools together. Keep it simple
for learning: the logic is explicit and easy to follow.
"""
import argparse
from typing import List
from .model import create_model, build_messages
from .tools import execute_tool, get_weather
from langchain_core.messages import HumanMessage


def run_query(user_prompt: str):
    """Run the given user prompt through the model + tool flow and print result."""
    model = create_model()

    # Bind the Python tool(s) so the model can call them by name.
    # `bind_tools` expects callables decorated via LangChain's tool system; in
    # our simple setup we rely on the model returning a tool name and args and
    # then execute the corresponding Python function with `execute_tool`.
    model_with_tools = model.bind_tools([get_weather])

    messages: List[HumanMessage] = build_messages(user_prompt)

    # Ask the model. It may either reply directly or request a tool call.
    response = model_with_tools.invoke(messages)

    # If the model requested a tool, execute it and give the result back to
    # the model so it can produce a final user-facing answer.
    if getattr(response, "tool_calls", None):
        for tool_call in response.tool_calls:
            # Execute using our mapped executor (keeps separation of concerns)
            tool_result = execute_tool(tool_call)

            # Feed the tool result back into the conversation for the LLM to
            # produce a final, nicely formatted reply.
            messages.append(HumanMessage(content=f"Tool {tool_call.get('name')} returned: {tool_result}"))
            final_response = model_with_tools.invoke(messages)

            # Extract text safely (different LangChain versions may vary).
            text = None
            try:
                text = final_response.generations[0][0].text
            except Exception:
                pass

            if not text:
                try:
                    text = final_response.generations[0][0].message.content
                except Exception:
                    pass

            if not text:
                text = getattr(final_response, "content", None)

            if not text:
                text = str(final_response)

            print(text)
    else:
        # No tools requested; print the model reply directly.
        try:
            print(response.generations[0][0].text)
        except Exception:
            print(response)


def main():
    parser = argparse.ArgumentParser(description="Weather agent CLI")
    parser.add_argument("city", nargs="?", default="Denver", help="City to fetch weather for")
    args = parser.parse_args()

    run_query(f"what is the weather in {args.city}")


if __name__ == "__main__":
    main()
