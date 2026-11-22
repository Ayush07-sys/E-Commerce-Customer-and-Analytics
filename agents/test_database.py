
import ollama
import psycopg2

# 1. Connect to PostgreSQL
connection = psycopg2.connect(
    host="localhost",
    port="5432",
    database="ecommerce_analytics",
    user="postgres",
    password="Kundan@123"
)

print("Database connection successful!")

# 2. Create cursor
cursor = connection.cursor()

# 3. Execute SQL query
cursor.execute("""
    SELECT
        customer_segment,
        COUNT(*) AS customer_count,
        ROUND(AVG(total_spending)::numeric, 2) AS avg_spending
    FROM analytics_dbt.dim_customers
    GROUP BY customer_segment
    ORDER BY avg_spending DESC;
""")

# 4. Retrieve results
results = cursor.fetchall()

# 5. Get column names
columns = [desc[0] for desc in cursor.description]

# 6. Convert results into readable text
data_for_ai = "\n".join(
    str(dict(zip(columns, row)))
    for row in results
)

# 7. Close database resources
cursor.close()
connection.close()

print("\nDatabase results retrieved successfully!")

# 8. Send actual database results to Qwen
response = ollama.chat(
    model="qwen3:4b",
    think=False,
    messages=[
        {
            "role": "system",
            "content": """You are an expert e-commerce business analyst.

            Analyze only the supplied database results.

            Rules:
            1. Respect SQL column names and meanings.
            2. AVG means average and SUM means total.
            3. Never divide or recalculate averages unless requested.
            4. Never confuse revenue, spending and profit.
            5. Never invent figures.
            6. Provide clear and concise business insights.
            """
        },
        {
            "role": "user",
            "content": f"""
            Analyze these actual customer segment results:

            {data_for_ai}

            Question:
            Which customer segment has the highest average spending?
            Explain the business insight.
            """
        }
    ]
)

# 9. Display AI analysis
print("\n========== AI BUSINESS ANALYST ==========\n")
print(response["message"]["content"])
