
"""Ask the LLM questions without giving it access to tools."""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

MODEL = os.getenv("MODEL", "openai/gpt-oss-20b")


def ask_without_tool(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful college fee assistant. "
                    "Answer clearly. Show calculation steps when needed."
                ),
            },
            {"role": "user", "content": question},
        ],
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    questions = [
        "What is an AI agent?",
        "What is the total fee for CS101 (12000) and AI202 (18000) after a 10% scholarship?",
        "What is the fee difference between DS303 (15000) and CS101 (12000)?",
    ]

    for question in questions:
        print("\nQuestion:", question)
        print("Answer:", ask_without_tool(question))
        print("-" * 60)
