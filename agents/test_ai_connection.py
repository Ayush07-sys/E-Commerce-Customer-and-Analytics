
import psycopg2
from getpass import getpass

# Ask for password securely
password = getpass("Enter ai_analyst password: ")

try:
    # Connect using the restricted account
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="ecommerce_analytics",
        user="ai_analyst",
        password=password,
        connect_timeout=5
    )

    # Enforce read-only transaction
    connection.set_session(readonly=True)

    print("\nDatabase connection successful!")

    cursor = connection.cursor()

    # Verify account and read-only status
    cursor.execute("""
        SELECT
            current_user,
            current_setting('transaction_read_only');
    """)

    user, read_only = cursor.fetchone()

    print("Database user:", user)
    print("Read-only mode:", read_only)

    # Test access to product performance
    cursor.execute("""
        SELECT COUNT(*)
        FROM analytics_dbt.fct_product_performance;
    """)

    product_count = cursor.fetchone()[0]

    print("Products accessible:", product_count)

    cursor.close()
    connection.rollback()
    connection.close()

    print("\nAI database connection test passed!")

except Exception as error:
    print("\nDatabase connection failed:", error)
