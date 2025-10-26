#!/usr/bin/env python3
"""
Full tool-calling test for vLLM + NVIDIA Nemotron-Nano-9B-v2

1. Ask the model a question.
2. Let the model decide to call a tool.
3. Execute the tool in Python.
4. Send the result back to the model for a final response.
"""

import json

from openai import OpenAI

# Connect to local vLLM server
client = OpenAI(base_url="http://localhost:8000/v1", api_key="dummy")


# Simple Python implementation of the tool
def calculate_tip(bill_total: float, tip_percentage: float) -> float:
    """Return the calculated tip amount."""
    return bill_total * (tip_percentage / 100.0)


# Define the tool schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_tip",
            "description": "Compute the tip amount for a restaurant bill.",
            "parameters": {
                "type": "object",
                "properties": {
                    "bill_total": {
                        "type": "number",
                        "description": "Total bill in dollars",
                    },
                    "tip_percentage": {
                        "type": "number",
                        "description": "Tip percent to apply",
                    },
                },
                "required": ["bill_total", "tip_percentage"],
            },
        },
    }
]

# Conversation messages
messages = [
    {"role": "system", "content": "/think You are a helpful assistant."},
    {"role": "user", "content": "My bill is $100. What is an 18% tip and total?"},
]

# === 1️⃣ Ask model, expect a tool call ===
response = client.chat.completions.create(
    model="nvidia/NVIDIA-Nemotron-Nano-9B-v2",
    messages=messages,
    tools=tools,
    tool_choice="auto",
    temperature=0.6,
    max_tokens=256,
)

msg = response.choices[0].message
print("\n=== Step 1: Tool Call ===")
print(msg.tool_calls or "[no tool call found]")

if not msg.tool_calls:
    print("❌ Model did not call any tool.")
    exit(1)

tool_call = msg.tool_calls[0]
tool_name = tool_call.function.name
args = json.loads(tool_call.function.arguments)
print(f"→ Calling tool: {tool_name}({args})")

# === 2️⃣ Run the tool locally ===
if tool_name == "calculate_tip":
    tip = calculate_tip(args["bill_total"], args["tip_percentage"])
    total = round(args["bill_total"] + tip, 2)
    tool_result = {"tip": round(tip, 2), "total": total}
else:
    tool_result = {"error": "unknown tool"}

print(f"→ Tool result: {tool_result}")

# === 3️⃣ Send result back to model ===
messages.extend(
    [
        {
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_name,
                        "arguments": json.dumps(args),
                    },
                }
            ],
        },
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_result),
        },
    ]
)

response_final = client.chat.completions.create(
    model="nvidia/NVIDIA-Nemotron-Nano-9B-v2",
    messages=messages,
    max_tokens=256,
    temperature=0.2,
)

print("\n=== Step 2: Final Model Answer ===")
print(response_final.choices[0].message.content.strip())
print("\n✅ Test complete.")
