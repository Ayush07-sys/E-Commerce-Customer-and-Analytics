
import pandas as pd
from pathlib import Path

# Project paths
base = Path(__file__).resolve().parent
raw = base / "data" / "raw"
output = base / "streamlit_public" / "data" / "financial_data.csv"

# Load source datasets
orders = pd.read_csv(raw / "orders.csv")
items = pd.read_csv(raw / "order_items.csv")
products = pd.read_csv(raw / "products.csv")

# Standardize order dates
orders["ordered_at"] = (
    pd.to_datetime(orders["ordered_at"], utc=True)
    .dt.tz_convert(None)
)

# Join tables
df = (
    items
    .merge(
        orders[["order_id", "ordered_at", "order_status"]],
        on="order_id"
    )
    .merge(
        products[["product_id", "product_name", "category", "unit_cost"]],
        on="product_id"
    )
)

# Match dbt financial logic
df = df[df["order_status"] != "cancelled"].copy()

df["product_revenue"] = df["line_total"]
df["product_cost"] = df["quantity"] * df["unit_cost"]
df["gross_profit"] = df["product_revenue"] - df["product_cost"]

# Calculate each product's overall margin
product_totals = df.groupby("product_id").agg(
    total_revenue=("product_revenue", "sum"),
    total_profit=("gross_profit", "sum")
)

product_totals["profit_margin"] = (
    product_totals["total_profit"]
    / product_totals["total_revenue"].replace(0, float("nan"))
    * 100
)

# Aggregate monthly product data
df["Month"] = df["ordered_at"].dt.to_period("M").dt.to_timestamp()

monthly = df.groupby(
    ["Month", "product_id", "product_name", "category"],
    as_index=False
).agg(
    product_revenue=("product_revenue", "sum"),
    product_cost=("product_cost", "sum"),
    gross_profit=("gross_profit", "sum")
)

# Attach product-level margin
monthly = monthly.merge(
    product_totals[["profit_margin"]],
    on="product_id"
)

# Save prepared dataset
monthly.to_csv(output, index=False)

print("Dataset created successfully!")
print("Rows:", len(monthly))
print("Saved to:", output)
print("Revenue:", round(monthly["product_revenue"].sum(), 2))
print("Cost:", round(monthly["product_cost"].sum(), 2))
print("Profit:", round(monthly["gross_profit"].sum(), 2))
