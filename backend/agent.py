
import os
from dotenv import load_dotenv
from openai import OpenAI
from tools import execute_tool, TOOL_FUNCTIONS

load_dotenv(override=True)

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

MODEL = "openrouter/free"

SYSTEM_PROMPT = """
You are Ask-and-Act, a helpful assistant.

You can use these tools:
- calculate: perform arithmetic calculations.
- get_weather: retrieve weather for a city.
- search_knowledge: search the local knowledge base.

Use tools when they are useful. You may call multiple tools if needed.
Do not invent tool results. If a question does not need a tool, answer normally.
Explain results clearly and concisely.
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Arithmetic expression to calculate"
                    }
                },
                "required": ["expression"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current forecast information for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["city"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "Search the project's local knowledge base.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "What to search for"
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }
    }
]


def ask_agent(message: str) -> dict:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": message},
    ]
    tools_used = []

    for _ in range(6):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        assistant_message = response.choices[0].message
        messages.append(assistant_message.model_dump(exclude_none=True))

        if not assistant_message.tool_calls:
            return {
                "answer": assistant_message.content or "I couldn't generate a response.",
                "tools_used": tools_used,
            }

        for tool_call in assistant_message.tool_calls:
            name = tool_call.function.name
            arguments = tool_call.function.arguments

            import json
            try:
                args = json.loads(arguments)
                result = execute_tool(name, args)
            except Exception as exc:
                result = {"error": str(exc)}

            if name not in tools_used:
                tools_used.append(name)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, default=str),
            })

    return {
        "answer": "I reached the tool-call limit. Please try a simpler request.",
        "tools_used": tools_used,
    }
