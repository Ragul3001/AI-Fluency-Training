
"""Ask the LLM questions with access to a calculator tool."""

import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from my_tools import calculator

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": (
                "Calculate a mathematical expression accurately. "
                "Use this for arithmetic involving course fees, "
                "scholarships, totals, and differences."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The arithmetic expression to calculate",
                    }
                },
                "required": ["expression"],
            },
        },
    }
]


def ask_with_tool(question):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a college fee assistant. "
                "Use the calculator tool for fee calculations. "
                "Explain the result clearly."
            ),
        },
        {"role": "user", "content": question},
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )

    message = response.choices[0].message

    if not message.tool_calls:
        return message.content or "No answer returned.", "No tool call"

    tool_results = []

    for tool_call in message.tool_calls:
        if tool_call.function.name != "calculator":
            continue

        arguments = json.loads(tool_call.function.arguments)
        expression = arguments["expression"]

        print("Tool called:", tool_call.function.name)
        print("Tool arguments:", arguments)

        result = calculator(expression)
        print("Tool result:", result)

        messages.append(
            {
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": "function",
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments,
                        },
                    }
                ],
            }
        )

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
        )

        tool_results.append(result)

    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )

    return (
        final_response.choices[0].message.content,
        "; ".join(tool_results),
    )


if __name__ == "__main__":
    questions = [
        "What is an AI agent?",
        (
            "What is the total fee for CS101 (12000) and AI202 "
            "(18000) after a 10% scholarship?"
        ),
        "What is the fee difference between DS303 (15000) and CS101 (12000)?",
    ]

    for question in questions:
        print("\nQuestion:", question)

        answer, tool_result = ask_with_tool(question)

        print("Tool result:", tool_result)
        print("Final answer:", answer)
        print("-" * 60)
