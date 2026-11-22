
import ollama

schema = """
Table: analytics_dbt.fct_product_performance
Columns:
- product_id
- product_name
- category
- total_units_sold
- total_orders
- total_revenue
- total_cost
- total_gross_profit
- profit_margin_percentage

Table: analytics_dbt.dim_customers
Columns:
- customer_id
- customer_segment
- total_orders
- total_spending
- average_order_value
- days_since_last_purchase

Table: analytics_dbt.mart_monthly_performance
Columns:
- order_month
- total_orders
- total_order_revenue
- total_product_revenue
- total_product_cost
- total_gross_profit
- profit_margin_percentage
"""

question = "Show each product category and its total gross profit, highest first."

response = ollama.chat(
    model="qwen3:4b",
    think=False,
    messages=[
        {
            "role": "system",
            "content": f"""
You are a PostgreSQL SQL expert.

Generate SQL using only the following schema:

{schema}

Rules:
1. Generate only SELECT queries.
2. Use only the supplied tables and columns.
3. Never use INSERT, UPDATE, DELETE or DROP.
4. Use the analytics_dbt schema.
5. Return SQL only, without explanations or Markdown.
6. Include a LIMIT clause.
"""
        },
        {
            "role": "user",
            "content": question
        }
    ]
)

generated_sql = response["message"]["content"].strip()

print("\nUSER QUESTION:")
print(question)

print("\nGENERATED SQL:")
print(generated_sql)
