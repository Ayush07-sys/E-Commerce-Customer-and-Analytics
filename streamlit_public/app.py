

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

    # Load prepared financial dataset
    data_path = Path(__file__).resolve().parent / "data" / "financial_data.csv"

    financial_df = pd.read_csv(
        data_path,
        parse_dates=["Month"]
    )

    # Financial Filters
    st.subheader("Financial Filters")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    available_months = sorted(
        financial_df["Month"].dt.to_period("M").unique()
    )
    month_labels = [str(month) for month in available_months]

    with filter_col1:
        start_month = st.selectbox(
            "Start Month", month_labels, index=0
        )
        end_month = st.selectbox(
            "End Month",
            month_labels,
            index=len(month_labels) - 1
        )

    with filter_col2:
        categories = sorted(financial_df["category"].dropna().unique())
        category = st.selectbox(
            "Product Category",
            ["All Categories"] + [c.title() for c in categories]
        )

    with filter_col3:
        margin_filter = st.selectbox(
            "Product Profit Margin",
            ["All Margins", "Below 40%", "40%-50%", "Above 50%"]
        )

    # Apply month range
    start_period = pd.Period(start_month, freq="M")
    end_period = pd.Period(end_month, freq="M")

    if start_period > end_period:
        st.warning("Start month cannot be later than end month.")
        filtered_data = financial_df.iloc[0:0].copy()
    else:
        month_periods = financial_df["Month"].dt.to_period("M")
        filtered_data = financial_df[
            (month_periods >= start_period)
            & (month_periods <= end_period)
        ].copy()

    # Apply category filter
    if category != "All Categories":
        filtered_data = filtered_data[
            filtered_data["category"] == category.lower()
        ]

    # Apply product-level margin filter
    if margin_filter == "Below 40%":
        filtered_data = filtered_data[
            filtered_data["profit_margin"] < 40
        ]
    elif margin_filter == "40%-50%":
        filtered_data = filtered_data[
            (filtered_data["profit_margin"] >= 40)
            & (filtered_data["profit_margin"] <= 50)
        ]
    elif margin_filter == "Above 50%":
        filtered_data = filtered_data[
            filtered_data["profit_margin"] > 50
        ]

    st.divider()

    if filtered_data.empty:
        st.warning("No data available for the selected filters.")
    else:
        # Dynamic KPIs
        total_revenue = filtered_data["product_revenue"].sum()
        total_cost = filtered_data["product_cost"].sum()
        total_profit = filtered_data["gross_profit"].sum()

        total_margin = (
            total_profit / total_revenue * 100
            if total_revenue > 0 else 0
        )

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Product Revenue",
            f"${total_revenue / 1_000_000:.2f}M"
        )
        col2.metric(
            "Total Gross Profit",
            f"${total_profit / 1_000_000:.2f}M"
        )
        col3.metric(
            "Total Product Cost",
            f"${total_cost / 1_000_000:.2f}M"
        )
        col4.metric(
            "Product Profit Margin",
            f"{total_margin:.2f}%"
        )

        st.caption(
            "Margin filtering uses each product's overall margin "
            "across the complete dataset. KPIs and charts reflect "
            "the selected month range, category and margin filters."
        )

        st.divider()

        # Monthly aggregation
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

        st.subheader("Monthly Product Revenue vs Gross Profit")
        st.line_chart(
            monthly_data[["Product Revenue", "Gross Profit"]]
        )

        st.subheader("Monthly Product Cost Trend")
        st.line_chart(monthly_data[["Product Cost"]])

        st.subheader("Monthly Gross Profit Trend")
        st.line_chart(monthly_data[["Gross Profit"]])


