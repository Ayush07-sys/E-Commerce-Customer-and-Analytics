

import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="E-Commerce Customer Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("E-Commerce Customer Analytics")
st.caption("Interactive public portfolio demo | Python • SQL • dbt • Power BI • Machine Learning")


# Navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "Executive Overview",
    "Product Performance",
    "Customer Analytics",
    "Revenue & Financial Analytics"
])


with tab1:
    st.subheader("Executive Overview")

    st.write("""
    This project analyzes e-commerce customer behavior, purchasing patterns,
    product profitability and revenue performance using an end-to-end
    analytics and machine learning workflow.
    """)

    # Executive Overview KPIs
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", "20K")
    col2.metric("Total Orders", "97K")
    col3.metric("Total Order Revenue", "$63.46M")
    col4.metric("Gross Gross Profit", "$29.60M")

    st.divider()

    # Monthly Revenue Trend
    st.subheader("Monthly Revenue Trend")

    monthly_data = pd.DataFrame({
        "Month": pd.date_range("2023-01-01", periods=37, freq="MS"),
        "Total Order Revenue": [
            1708458, 1628965, 1906024, 1769465, 1760724, 1671294,
            1788440, 1703890, 1732815, 1819968, 1781911, 1767785,
            1765896, 1731408, 1819834, 1691802, 1771288, 1756151,
            1797445, 1868740, 1738078, 1757451, 1744150, 1740654,
            1769004, 1670118, 1835087, 1730578, 1811789, 1756785,
            1788892, 1812760, 1724159, 1777049, 1760517, 1786644,
            12543.93
        ]
    }).set_index("Month")

    st.line_chart(monthly_data)

    st.divider()

    # Monthly Revenue vs Gross Profit
    st.subheader("Monthly Revenue vs Gross Profit")

    comparison_data = pd.DataFrame({
        "Month": pd.date_range("2023-01-01", periods=37, freq="MS"),
        "Total Order Revenue": [
            1708457.89, 1628964.88, 1906024.15, 1769465.09,
            1760723.83, 1671294.44, 1788439.70, 1703890.08,
            1732815.23, 1819967.82, 1781910.63, 1767784.81,
            1765895.79, 1731408.08, 1819834.05, 1691802.31,
            1771288.20, 1756150.83, 1797445.41, 1868739.97,
            1738077.98, 1757450.90, 1744150.38, 1740653.81,
            1769004.17, 1670117.89, 1835087.11, 1730577.62,
            1811789.02, 1756785.35, 1788892.41, 1812760.21,
            1724158.89, 1777048.65, 1760517.44, 1786643.72,
            12543.93
        ],
        "Gross Product Profit": [
            799385.87, 760276.12, 893128.67, 828640.25,
            823051.27, 777038.16, 831376.70, 793286.15,
            806702.78, 849523.56, 830123.23, 825388.71,
            822253.34, 811887.54, 847352.57, 789520.88,
            825952.92, 818412.85, 834843.58, 873333.20,
            812344.54, 819419.27, 817382.32, 817208.03,
            823122.08, 773652.79, 857489.41, 804604.15,
            847555.49, 820633.71, 829434.43, 842105.54,
            802709.40, 831322.32, 819792.04, 830559.41,
            5687.43
        ]
    }).set_index("Month")

    st.line_chart(comparison_data)



with tab2:
    st.subheader("Product Performance")

    profit_by_category = pd.DataFrame({
        "Category": [
            "electronics", "apparel", "outdoors",
            "office", "beauty", "home"
        ],
        "Gross Profit": [
            5081935.97, 5032407.24, 4974717.92,
            4949368.58, 4891901.17, 4666169.83
        ]
    })

    revenue_by_category = pd.DataFrame({
        "Category": [
            "apparel", "outdoors", "electronics",
            "beauty", "office", "home"
        ],
        "Revenue": [
            10070386.43, 9930336.66, 9903329.52,
            9871192.14, 9668292.90, 9276323.49
        ]
    })

    top_products = pd.DataFrame({
        "Product": [
            "Apparel Item 0733",
            "Electronics Item 0536",
            "Home Item 0261",
            "Beauty Item 0257",
            "Home Item 0477",
            "Electronics Item 0068",
            "Electronics Item 1010",
            "Home Item 0039",
            "Office Item 0816",
            "Office Item 0402"
        ],
        "Gross Profit": [
            84320.84, 83436.47, 83064.96, 80191.14,
            79255.75, 77490.43, 75548.83, 75541.15,
            75343.96, 75222.76
        ]
    })

    left, right = st.columns(2)

    with left:
        st.subheader("Top 10 Products by Gross Profit")
        st.bar_chart(
            top_products.set_index("Product"),
            horizontal=True
        )

        st.subheader("Revenue by Product Category")
        st.bar_chart(
            revenue_by_category.set_index("Category")
        )

    with right:
        st.subheader("Gross Profit by Product Category")
        st.bar_chart(
            profit_by_category.set_index("Category")
        )


with tab3:
    st.subheader("Customer Analytics")

    # Customer KPI Cards
    col1, col2, col3 = st.columns(3)

    col1.metric("Purchasing Customers", "19.85K")
    col2.metric("Repeat Customers", "19.017K")
    col3.metric("Overall Repeat Customer Rate", "95.8%")

    st.divider()

    # Chart 1: Revenue by Customer Segment
    st.subheader("Revenue by Customer Segment")

    revenue_segment = pd.DataFrame({
        "Customer Segment": [
            "Consumer", "Small Business", "Enterprise"
        ],
        "Total Revenue": [
            52075731, 9482925, 1899907
        ]
    }).set_index("Customer Segment")

    st.bar_chart(revenue_segment)

    st.divider()

    # Chart 2: Customer Distribution by Segment
    st.subheader("Customer Distribution by Segment")

    customer_types = pd.DataFrame({
        "Customer Type": [
            "Consumer", "Small Business", "Enterprise"
        ],
        "Customers": [16407, 2989, 604]
    }).set_index("Customer Type")

    st.bar_chart(customer_types)

    st.divider()

    # Chart 3: Repeat Customer Rate by Segment
    st.subheader("Repeat Customer Rate by Segment")

    repeat_rate = pd.DataFrame({
        "Customer Segment": [
            "Consumer", "Enterprise", "Small Business"
        ],
        "Repeat Customer Rate (%)": [
            95.85, 95.67, 95.60
        ]
    }).set_index("Customer Segment")

    st.bar_chart(repeat_rate)

    st.divider()

    # K-Means Customer Segmentation
    st.subheader("K-Means Customer Segmentation")

    segment_details = pd.DataFrame({
        "Behavior Segment": [
            "High Value Frequent", "Regular", "At Risk"
        ],
        "Customers": [6418, 9955, 3477],
        "Average Orders": [7.30, 4.04, 2.88],
        "Average Spend ($)": [5191.13, 2394.89, 1812.12]
    })

    st.dataframe(
        segment_details,
        hide_index=True,
        use_container_width=True
    )

    st.caption(
        "Customer types and behavioral segments are two different "
        "classifications."
    )




with tab4:
    st.subheader("Revenue & Financial Analytics")

    # Load original project datasets
    data_path = Path(__file__).resolve().parent.parent / "data" / "raw"

    orders = pd.read_csv(
        data_path / "orders.csv",
        parse_dates=["ordered_at"]
    )

    order_items = pd.read_csv(data_path / "order_items.csv")
    products = pd.read_csv(data_path / "products.csv")

    # Convert dates to consistent timezone-naive timestamps
    orders["ordered_at"] = (
        pd.to_datetime(orders["ordered_at"], utc=True)
        .dt.tz_convert(None)
    )

    # Join the three datasets
    financial_df = (
        order_items
        .merge(
            orders[["order_id", "ordered_at", "order_status"]],
            on="order_id",
            how="inner"
        )
        .merge(
            products[["product_id", "product_name", "category", "unit_cost"]],
            on="product_id",
            how="inner"
        )
    )

    # Exclude cancelled orders, matching the dbt model
    financial_df = financial_df[
        financial_df["order_status"] != "cancelled"
    ].copy()

    # Calculate financial metrics
    financial_df["product_revenue"] = financial_df["line_total"]
    financial_df["product_cost"] = (
        financial_df["quantity"] * financial_df["unit_cost"]
    )
    financial_df["gross_profit"] = (
        financial_df["product_revenue"] - financial_df["product_cost"]
    )

    # Calculate overall product-level margins
    product_margins = (
        financial_df.groupby("product_id")
        .agg(
            revenue=("product_revenue", "sum"),
            profit=("gross_profit", "sum")
        )
    )

    product_margins["margin"] = (
        product_margins["profit"]
        / product_margins["revenue"].replace(0, float("nan"))
        * 100
    )

    # Financial Filters
    st.subheader("Financial Filters")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    min_date = financial_df["ordered_at"].min().date()
    max_date = financial_df["ordered_at"].max().date()

    with filter_col1:
        selected_dates = st.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            format="DD/MM/YYYY"
        )

    with filter_col2:
        categories = sorted(financial_df["category"].dropna().unique())

        category = st.selectbox(
            "Select Product Category",
            ["All Categories"] + [
                c.title() for c in categories
            ]
        )

    with filter_col3:
        profit_margin = st.selectbox(
            "Select Profit Margin",
            [
                "All Margins",
                "Below 40%",
                "40%-50%",
                "Above 50%"
            ]
        )

    # Validate selected date range
    if len(selected_dates) == 2:
        start_date, end_date = selected_dates
    else:
        start_date = selected_dates[0]
        end_date = selected_dates[0]

    # Apply date filter
    filtered_data = financial_df[
        (financial_df["ordered_at"].dt.date >= start_date)
        & (financial_df["ordered_at"].dt.date <= end_date)
    ].copy()

    # Apply category filter
    if category != "All Categories":
        filtered_data = filtered_data[
            filtered_data["category"] == category.lower()
        ]

    # Apply product-level profit margin filter
    if profit_margin == "Below 40%":
        selected_products = product_margins[
            product_margins["margin"] < 40
        ].index

    elif profit_margin == "40%-50%":
        selected_products = product_margins[
            (product_margins["margin"] >= 40)
            & (product_margins["margin"] <= 50)
        ].index

    elif profit_margin == "Above 50%":
        selected_products = product_margins[
            product_margins["margin"] > 50
        ].index

    else:
        selected_products = product_margins.index

    filtered_data = filtered_data[
        filtered_data["product_id"].isin(selected_products)
    ]

    st.divider()

    # Dynamic KPI calculations
    total_revenue = filtered_data["product_revenue"].sum()
    total_cost = filtered_data["product_cost"].sum()
    total_profit = filtered_data["gross_profit"].sum()

    total_margin = (
        (total_profit / total_revenue * 100)
        if total_revenue > 0 else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Product Revenue",
        f"${total_revenue:,.2f}"
    )

    col2.metric(
        "Total Gross Profit",
        f"${total_profit:,.2f}"
    )

    col3.metric(
        "Total Product Cost",
        f"${total_cost:,.2f}"
    )

    st.metric("Product Profit Margin", f"{total_margin:.2f}%")

    st.caption(
        "Profit margin filtering uses each product's overall margin "
        "across the available dataset. KPIs and charts reflect the "
        "selected date range, category and margin filters."
    )

    st.divider()

    # Aggregate filtered data by month
    if filtered_data.empty:
        st.warning("No data available for the selected filters.")

    else:
        filtered_data["Month"] = (
            filtered_data["ordered_at"]
            .dt.to_period("M")
            .dt.to_timestamp()
        )

        monthly_data = (
            filtered_data.groupby("Month")
            .agg(
                **{
                    "Product Revenue": ("product_revenue", "sum"),
                    "Gross Profit": ("gross_profit", "sum"),
                    "Product Cost": ("product_cost", "sum")
                }
            )
            .sort_index()
        )

        # Chart 1
        st.subheader("Monthly Product Revenue vs Gross Profit")

        st.line_chart(
            monthly_data[
                ["Product Revenue", "Gross Profit"]
            ]
        )

        # Chart 2
        st.subheader("Monthly Product Cost Trend")

        st.line_chart(
            monthly_data[["Product Cost"]]
        )

        # Chart 3
        st.subheader("Monthly Gross Profit Trend")

        st.line_chart(
            monthly_data[["Gross Profit"]]
        )

