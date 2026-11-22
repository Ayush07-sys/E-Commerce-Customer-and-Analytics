
import sqlglot
from sqlglot import exp

sql = """
SELECT
    category,
    SUM(total_gross_profit) AS total_gross_profit
FROM analytics_dbt.fct_product_performance
GROUP BY category
ORDER BY total_gross_profit DESC
LIMIT 100
"""

allowed_tables = {
    "fct_product_performance",
    "dim_customers",
    "mart_monthly_performance"
}

try:
    # Step 1: Parse the SQL
    statements = sqlglot.parse(sql, read="postgres")

    # Step 2: Allow only one SQL statement
    if len(statements) != 1:
        raise ValueError("Only one SQL statement is allowed.")

    query = statements[0]

    # Step 3: Allow only SELECT queries
    if not isinstance(query, exp.Select):
        raise ValueError("Only SELECT queries are allowed.")

    # Step 4: Disallow CTEs
    if query.args.get("with"):
        raise ValueError("CTEs are not allowed.")

    # Step 5: Require LIMIT
    if query.args.get("limit") is None:
        raise ValueError("A LIMIT clause is required.")

    # Step 6: Enforce maximum LIMIT of 100
    limit_value = query.args["limit"].expression

    if not isinstance(limit_value, exp.Literal) or not limit_value.is_int:
        raise ValueError("LIMIT must be a fixed integer.")

    if int(limit_value.this) < 1 or int(limit_value.this) > 100:
        raise ValueError("LIMIT must be between 1 and 100.")

    # Step 7: Validate table names and schema
    tables = list(query.find_all(exp.Table))

    if not tables:
        raise ValueError("Query must reference an allowed table.")

    for table in tables:
        if table.db.lower() != "analytics_dbt":
            raise ValueError("Only analytics_dbt tables are allowed.")

        if table.name.lower() not in allowed_tables:
            raise ValueError(f"Table not allowed: {table.name}")

    # Step 8: Validation successful
    print("SQL validation successful!")
    print("\nValidated SQL:")
    print(query.sql(dialect="postgres"))

except Exception as error:
    print("SQL validation failed:", error)
