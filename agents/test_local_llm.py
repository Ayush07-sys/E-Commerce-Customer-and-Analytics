import ollama

response = ollama.chat(
    model="qwen3:4b",
    messages=[
    {
        "role": "system",
        "content": """You are an expert e-commerce business analyst. Explain insights clearly using business language. Use this actual customer segmentation data:
High Value Frequent: 6418 customers, average spending $5191.13.
At Risk: 3477 customers, average spending $1812.12.
Regular: 9955 customers, average spending $2394.89.

Never invent figures. Base your recommendations on the supplied data.
Do not make unsupported claims about profitability,
ROI, revenue contribution, or customer lifetime value.
Clearly distinguish calculated facts from assumptions.
Never recommend arbitrary budget percentages."""
    },
    {
        "role": "user",
        "content": "Which customer segment should the business prioritize and why?"
    }
]
)

print(response["message"]["content"])