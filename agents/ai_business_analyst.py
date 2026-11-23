
import ollama
import psycopg2
import sqlglot
import re
import json

from getpass import getpass
from sqlglot import exp


# ============================================
# 1. DATABASE SCHEMA
# ============================================

schema = """
Table: analytics_dbt.fct_product_performance
Columns:
product_id, product_name, category, total_units_sold,
total_orders, total_revenue, total_cost,
total_gross_profit, profit_margin_percentage

Table: analytics_dbt.dim_customers
Columns:
customer_id, country_code, acquisition_channel,
customer_segment, created_at, total_orders,
total_spending, average_order_value,
first_purchase_date, last_purchase_date,
days_since_last_purchase

Table: analytics_dbt.mart_monthly_performance
Columns:
order_month, total_orders, total_order_revenue,
total_product_revenue, total_product_cost,
total_gross_profit, profit_margin_percentage
"""


# ============================================
# 2. SECURITY CONFIGURATION
# ============================================

allowed_tables = {
    "fct_product_performance",
    "dim_customers",
    "mart_monthly_performance"
}

allowed_columns = {
    "fct_product_performance": {
        "product_id", "product_name", "category",
        "total_units_sold", "total_orders",
        "total_revenue", "total_cost",
        "total_gross_profit", "profit_margin_percentage"
    },
    "dim_customers": {
        "customer_id", "country_code", "acquisition_channel",
        "customer_segment", "created_at", "total_orders",
        "total_spending", "average_order_value",
        "first_purchase_date", "last_purchase_date",
        "days_since_last_purchase"
    },
    "mart_monthly_performance": {
        "order_month", "total_orders", "total_order_revenue",
        "total_product_revenue", "total_product_cost",
        "total_gross_profit", "profit_margin_percentage"
    }
}

allowed_functions = {
    "SUM", "AVG", "COUNT", "MIN", "MAX",
    "ROUND", "COALESCE", "DATE_TRUNC", "NULLIF"
}


# ============================================
# 3. GENERATE SQL USING QWEN
# ============================================

def generate_sql(question):

    response = ollama.chat(
        model="qwen3:4b",
        think=False,
        messages=[
            {
                "role": "system",
                "content": f"""
You are a PostgreSQL SQL generator.

Database schema:

{schema}

Rules:
1. Generate exactly one SELECT query.
2. Use only the supplied tables and columns.
3. Never generate INSERT, UPDATE, DELETE or DROP.
4. Do not use CTEs, subqueries or JOINs.
5. Always include LIMIT between 1 and 100.
6. For category-level gross profit, use
   SUM(total_gross_profit) GROUP BY category.
7. Use correct aggregation for business questions.
8. Return SQL only. No explanations or reasoning.
9. Include the aggregated metric in SELECT when ranking results.
10. 10. When comparing gross profit margin across categories, calculate
    (SUM(total_gross_profit) / NULLIF(SUM(total_revenue), 0)) * 100.
    Do not use MAX(profit_margin_percentage) or AVG(profit_margin_percentage)
    to calculate category-level gross profit margin.
"""
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    sql = response["message"]["content"].strip()

    # Remove reasoning section if present
    if "</think>" in sql:
        sql = sql.rsplit("</think>", 1)[1].strip()

    # Remove Markdown fences
    sql = re.sub(
        r"```(?:sql)?",
        "",
        sql,
        flags=re.IGNORECASE
    ).strip()

    # Extract SELECT statement
    match = re.search(
        r"\bSELECT\b.*",
        sql,
        re.IGNORECASE | re.DOTALL
    )

    if not match:
        raise ValueError("Qwen did not generate a SELECT query.")

    return match.group(0).strip()


# ============================================
# 4. VALIDATE GENERATED SQL
# ============================================

def validate_sql(sql):

    statements = sqlglot.parse(sql, read="postgres")

    if len(statements) != 1:
        raise ValueError("Only one SQL statement is allowed.")

    query = statements[0]

    if not isinstance(query, exp.Select):
        raise ValueError("Only SELECT queries are allowed.")

    # Reject CTEs, subqueries, joins and set operations
    if query.args.get("with"):
        raise ValueError("CTEs are not allowed.")

    if query.find(exp.Subquery):
        raise ValueError("Subqueries are not allowed.")

    if query.find(exp.Join):
        raise ValueError("JOINs are not allowed.")

    if query.find(exp.Union) or query.find(exp.Intersect) or query.find(exp.Except):
        raise ValueError("Set operations are not allowed.")

    # Require LIMIT
    if query.args.get("limit") is None:
        raise ValueError("LIMIT is required.")

    limit_value = query.args["limit"].expression

    if not isinstance(limit_value, exp.Literal) or not limit_value.is_int:
        raise ValueError("LIMIT must be a fixed integer.")

    limit_number = int(limit_value.this)

    if not 1 <= limit_number <= 100:
        raise ValueError("LIMIT must be between 1 and 100.")

    # Only one approved table
    tables = list(query.find_all(exp.Table))

    if len(tables) != 1:
        raise ValueError("Exactly one approved table is required.")

    table = tables[0]

    if table.db.lower() != "analytics_dbt":
        raise ValueError("Unauthorized schema.")

    table_name = table.name.lower()

    if table_name not in allowed_tables:
        raise ValueError("Unauthorized table.")

    # Reject SELECT INTO and locking clauses
    if query.args.get("into") or query.args.get("locks"):
        raise ValueError("This query contains a prohibited clause.")

    # Validate columns
    valid_columns = allowed_columns[table_name]

    output_aliases = {
        item.alias.lower()
        for item in query.expressions
        if isinstance(item, exp.Alias)
    }

    for column in query.find_all(exp.Column):

        if column.name.lower() not in valid_columns | output_aliases:
            raise ValueError(
                f"Unauthorized column: {column.name}"
            )

    # Reject SELECT *
    # COUNT(*) is permitted
    for star in query.find_all(exp.Star):

        if not isinstance(star.parent, exp.Count):
            raise ValueError("SELECT * is not allowed.")

    # Restrict SQL functions
    for function in query.find_all(exp.Func):

        function_name = function.sql_name().upper()

        if isinstance(function, exp.Anonymous):
            function_name = function.name.upper()

        if function_name not in allowed_functions:
            raise ValueError(
                f"Unauthorized SQL function: {function_name}"
            )

    return query.sql(dialect="postgres")


# ============================================
# 5. EXECUTE SQL IN POSTGRESQL
# ============================================

def execute_sql(sql, password):

    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="ecommerce_analytics",
        user="ai_analyst",
        password=password,
        connect_timeout=5
    )

    try:

        # Enforce read-only transaction
        connection.set_session(readonly=True)

        cursor = connection.cursor()

        cursor.execute(sql)

        results = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ]

        # Convert results into dictionaries
        data = [
            dict(zip(columns, row))
            for row in results
        ]

        cursor.close()

        return data

    finally:

        connection.rollback()
        connection.close()


# ============================================
# 6. ASK QWEN TO EXPLAIN REAL RESULTS
# ============================================


def explain_results(question, sql, results):
    data = json.dumps(results, default=str, indent=2)

    response = ollama.chat(
        model="qwen3:4b",
        think=False,
        messages=[
            {
                "role": "system",
                "content": """
You are an expert e-commerce business analyst.
Analyze only the supplied SQL results.
Rules:
1. Use only the actual supplied figures.
2. Never invent numbers.
3. Do not confuse revenue with gross profit.
4. Explain important business insights.
5. Be concise and professional.
6. Do not show internal reasoning.
7. If results are empty, clearly say no records were returned.
8. Never infer causes such as pricing power, operational efficiency,
   or product mix unless the query results directly support them.
9. Always distinguish total gross profit from gross profit margin.
   Only make claims supported by the SQL results.
"""
            },
            {
                "role": "user",
                "content": f"""
Business question:
{question}

SQL executed:
{sql}

Actual PostgreSQL results:
{data}

Explain the answer and its business significance.
"""
            }
        ]
    )

    answer = response["message"]["content"].strip()

    if "</think>" in answer:
        answer = answer.rsplit("</think>", 1)[1].strip()

    return answer


# ============================================
# 7. MAIN APPLICATION
# ============================================

def main():

    print("\n======================================")
    print("       AI E-COMMERCE BUSINESS ANALYST")
    print("======================================")

    password = getpass("\nEnter ai_analyst database password: ")

    question = input("\nAsk your business question: ").strip()

    if not question:
        print("Please enter a business question.")
        return

    try:

        # Generate SQL
        print("\n[1/4] Generating SQL using Qwen...")

        generated_sql = generate_sql(question)

        print("\nGenerated SQL:")
        print(generated_sql)

        # Validate SQL
        print("\n[2/4] Validating SQL...")

        validated_sql = validate_sql(generated_sql)

        print("SQL validation successful!")

        # Execute SQL
        print("\n[3/4] Executing SQL in PostgreSQL...")

        results = execute_sql(validated_sql, password)

        print("\nActual database results:")

        if results:
            for row in results:
                print(row)
        else:
            print("No records found.")

        # Explain results
        print("\n[4/4] Asking Qwen to analyze results...")

        answer = explain_results(
            question,
            validated_sql,
            results
        )

        print("\n======================================")
        print("          AI BUSINESS INSIGHTS")
        print("======================================")

        print(answer)

    except Exception as error:

        print("\nAPPLICATION ERROR:")
        print(error)


if __name__ == "__main__":
    main()
