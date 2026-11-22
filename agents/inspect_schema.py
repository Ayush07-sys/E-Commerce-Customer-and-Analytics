
import psycopg2

connection = psycopg2.connect(
    host="localhost",
    port="5432",
    database="ecommerce_analytics",
    user="postgres",
    password="Kundan@123"
)

cursor = connection.cursor()

cursor.execute("""
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'analytics_dbt'
      AND table_name IN (
          'fct_product_performance',
          'mart_monthly_performance',
          'dim_customers'
      )
    ORDER BY table_name, ordinal_position;
""")

for row in cursor.fetchall():
    print(row)

cursor.close()
connection.close()
