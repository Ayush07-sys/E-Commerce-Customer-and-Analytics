
import ollama
import sqlglot
import re
from sqlglot import exp


# ==========================================
# 1. DATABASE SCHEMA
# ==========================================

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


# ==========================================
# 2. ALLOWED TABLES
# ==========================================

allowed_tables = {
    "fct_product_performance",
    "dim_customers",
    "mart_monthly_performance"
}


# ==========================================
# 3. GET USER QUESTION
# ==========================================

question = input("Ask your business question: ")


# ==========================================
# 4. GENERATE SQL USING QWEN
# ==========================================

print("\nGenerating SQL using Qwen...")

response = ollama.chat(
    model="qwen3:4b",
    think=False,
    messages=[
        {
            "role": "system",
            "content": f"""
You are a PostgreSQL SQL generator.

Use only this database schema:

{schema}

Rules:
1. Return exactly one PostgreSQL SELECT query.
2. Never provide explanations or reasoning.
3. Use only the supplied tables and columns.
4. Never generate INSERT, UPDATE, DELETE or DROP.
5. Do not use CTEs or subqueries.
6. Always include LIMIT between 1 and 100.
7. For category-level gross profit, use
   SUM(total_gross_profit) GROUP BY category.
8. Return SQL only.
"""
        },
        {
            "role": "user",
            "content": question
        }
    ]
)


# ==========================================
# 5. CLEAN GENERATED SQL
# ==========================================

generated_sql = response["message"]["content"].strip()

# Remove Qwen reasoning section if present
if "</think>" in generated_sql:
    generated_sql = generated_sql.rsplit("</think>", 1)[1].strip()

# Remove Markdown code fences
generated_sql = re.sub(
    r"```(?:sql)?",
    "",
    generated_sql,
    flags=re.IGNORECASE
).strip()

# Extract SQL statement
match = re.search(
    r"\bSELECT\b.*",
    generated_sql,
    re.IGNORECASE | re.DOTALL
)

if not match:
    raise ValueError("No SQL SELECT query was generated.")

generated_sql = match.group(0).strip()

print("\n========== GENERATED SQL ==========")
print(generated_sql)


# ==========================================
# 6. VALIDATE GENERATED SQL
# ==========================================

try:

    # Parse SQL using PostgreSQL dialect
    statements = sqlglot.parse(
        generated_sql,
        read="postgres"
    )

    # Only one statement allowed
    if len(statements) != 1:
        raise ValueError("Only one SQL statement is allowed.")

    query = statements[0]

    # Only SELECT queries allowed
    if not isinstance(query, exp.Select):
        raise ValueError("Only SELECT queries are allowed.")

    # Reject CTEs
    if query.args.get("with"):
        raise ValueError("CTEs are not allowed.")

    # Reject subqueries
    if query.find(exp.Subquery):
        raise ValueError("Subqueries are not allowed.")

    # Require LIMIT
    if query.args.get("limit") is None:
        raise ValueError("LIMIT clause is required.")

    # Validate LIMIT value
    limit_value = query.args["limit"].expression

    if not isinstance(limit_value, exp.Literal) or not limit_value.is_int:
        raise ValueError("LIMIT must be a fixed integer.")

    limit_number = int(limit_value.this)

    if limit_number < 1 or limit_number > 100:
        raise ValueError("LIMIT must be between 1 and 100.")

    # Validate table references
    tables = list(query.find_all(exp.Table))

    if not tables:
        raise ValueError("At least one allowed table is required.")

    for table in tables:

        if table.db.lower() != "analytics_dbt":
            raise ValueError("Only analytics_dbt schema is allowed.")

        if table.name.lower() not in allowed_tables:
            raise ValueError(
                f"Unauthorized table: {table.name}"
            )

    # Validation successful
    print("\n========== SQL VALIDATION ==========")
    print("SQL validation successful!")
    print("Query type: SELECT")
    print("Schema: analytics_dbt")
    print(f"Maximum rows: {limit_number}")

    print("\nValidated SQL:")
    print(query.sql(dialect="postgres"))

except Exception as error:

    print("\n========== SQL VALIDATION ==========")
    print("SQL validation failed:", error)
