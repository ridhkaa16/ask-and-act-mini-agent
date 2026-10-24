
import ast
import json
import operator
import re
from pathlib import Path

import requests


# Locate knowledge.json relative to this Python file
KNOWLEDGE_FILE = Path(__file__).parent / "knowledge.json"


# ---------- Tool 1: Calculator ----------

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def calculate(expression: str) -> dict:
    """Calculate a basic arithmetic expression safely."""

    try:
        if len(expression) > 100:
            raise ValueError("Expression is too long.")

        tree = ast.parse(expression, mode="eval")

        def evaluate(node):
            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant) and type(node.value) in (int, float):
                return node.value

            if isinstance(node, ast.BinOp):
                operation = _ALLOWED_OPERATORS.get(type(node.op))
                if operation is None:
                    raise ValueError("Operator not allowed.")

                left = evaluate(node.left)
                right = evaluate(node.right)

                if isinstance(node.op, ast.Pow) and abs(right) > 10:
                    raise ValueError("Exponent is too large.")

                result = operation(left, right)

                if abs(result) > 1e100:
                    raise ValueError("Result is too large.")

                return result

            if isinstance(node, ast.UnaryOp):
                operation = _ALLOWED_OPERATORS.get(type(node.op))
                if operation is None:
                    raise ValueError("Unary operator not allowed.")
                return operation(evaluate(node.operand))

            raise ValueError("Invalid arithmetic expression.")

        return {
            "expression": expression,
            "result": evaluate(tree),
        }

    except (ValueError, TypeError, ZeroDivisionError, OverflowError, SyntaxError) as exc:
        return {"error": f"Calculator error: {exc}"}


# ---------- Tool 2: Weather ----------

def get_weather(city: str) -> dict:
    """Fetch today's high and low temperature using Open-Meteo."""

    try:
        geo_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en"},
            timeout=10,
        )
        geo_response.raise_for_status()

        locations = geo_response.json().get("results", [])

        if not locations:
            return {"error": f"City not found: {city}"}

        location = locations[0]

        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "daily": "temperature_2m_max,temperature_2m_min",
                "timezone": "auto",
                "forecast_days": 1,
            },
            timeout=10,
        )
        weather_response.raise_for_status()

        daily = weather_response.json()["daily"]

        return {
            "city": location["name"],
            "date": daily["time"][0],
            "high_c": daily["temperature_2m_max"][0],
            "low_c": daily["temperature_2m_min"][0],
            "units": "Celsius",
            "source": "Open-Meteo",
        }

    except (requests.RequestException, KeyError, IndexError, ValueError) as exc:
        return {"error": f"Weather lookup failed: {exc}"}


# ---------- Tool 3: Knowledge search ----------

def search_knowledge(query: str) -> dict:
    """Find relevant Q&A entries using keyword overlap."""

    try:
        with KNOWLEDGE_FILE.open("r", encoding="utf-8") as file:
            documents = json.load(file)

        query_words = set(re.findall(r"\w+", query.lower()))
        matches = []

        for document in documents:
            combined_text = (
                document["question"] + " " + document["answer"]
            ).lower()

            document_words = set(re.findall(r"\w+", combined_text))
            score = len(query_words & document_words)

            if score > 0:
                matches.append({
                    "question": document["question"],
                    "answer": document["answer"],
                    "score": score,
                })

        matches.sort(key=lambda item: item["score"], reverse=True)

        return {
            "query": query,
            "results": matches[:3],
        }

    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        return {"error": f"Knowledge search failed: {exc}"}


# ---------- Tool registry ----------

TOOL_FUNCTIONS = {
    "calculate": calculate,
    "get_weather": get_weather,
    "search_knowledge": search_knowledge,
}


def execute_tool(name: str, arguments: dict) -> dict:
    """Execute a tool by name, handling invalid calls."""

    function = TOOL_FUNCTIONS.get(name)

    if function is None:
        return {"error": f"Unknown tool: {name}"}

    try:
        return function(**arguments)
    except (TypeError, ValueError) as exc:
        return {"error": f"Invalid arguments for {name}: {exc}"}
