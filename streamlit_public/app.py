

import streamlit as st
import pandas as pd

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

    col1.metric("Total Customers", "20,000")
    col2.metric("Total Orders", "~97,000")
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

    # Financial KPI Cards
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Product Revenue", "$58.72M")
    col2.metric("Total Gross Profit", "$29.60M")
    col3.metric("Total Product Cost", "$29.12M")

    st.divider()

    # Slicers
    st.subheader("Financial Filters")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        date_range = st.selectbox(
            "Select Date Range",
            ["All Dates", "2023", "2024", "2025", "2026"]
        )

    with filter_col2:
        category = st.selectbox(
            "Select Product Category",
            ["All Categories", "Apparel", "Electronics",
             "Home", "Outdoors", "Beauty", "Office"]
        )

    with filter_col3:
        profit_margin = st.selectbox(
            "Select Profit Margin",
            ["All Margins", "Below 40%", "40%–50%", "Above 50%"]
        )

    st.divider()

    # Monthly financial data
    financial_data = pd.DataFrame({
        "Month": pd.date_range("2023-01-01", periods=37, freq="MS"),
        "Product Revenue": [
            1580970, 1507263, 1763861, 1637267, 1629212, 1546490,
            1654853, 1576703, 1603537, 1684014, 1648800, 1635659,
            1633909, 1602322, 1684000, 1565503, 1638922, 1625063,
            1663118, 1729419, 1608163, 1626239, 1613861, 1610760,
            1637040, 1545536, 1698054, 1601269, 1676508, 1625512,
            1655322, 1677411, 1595195, 1644337, 1629038, 1653122,
            11607.36
        ],
        "Gross Profit": [
            799385.9, 760276.1, 893128.7, 828640.3, 823051.3,
            777038.2, 831376.7, 793286.2, 806702.8, 849523.6,
            830123.2, 825388.7, 822253.3, 811887.5, 847352.6,
            789520.9, 825952.9, 818412.9, 834843.6, 873333.2,
            812344.5, 819419.3, 817382.3, 817208, 823122.1,
            773652.8, 857489.4, 804604.2, 847555.5, 820633.7,
            829434.4, 842105.5, 802709.4, 831322.3, 819792,
            830559.4, 5687.43
        ],
        "Product Cost": [
            781584, 746987.1, 870731.9, 808626.9, 806161.2,
            769452.3, 823476.4, 783417.1, 796834.6, 834490.6,
            818676.9, 810270.7, 811655.4, 790434, 836647.2,
            775982.5, 812969.1, 806650.2, 828274.1, 856086.1,
            795818.2, 806820.1, 796478.7, 793552.3, 813918,
            771883.3, 840564.7, 796665.2, 828952.1, 804878.2,
            825887.9, 835305.1, 792485.5, 813014.8, 809245.9,
            822562.2, 5919.93
        ]
    })

    # Apply date filter
    filtered_data = financial_data.copy()

    if date_range != "All Dates":
        filtered_data = filtered_data[
            filtered_data["Month"].dt.year.astype(str) == date_range
        ]

    # Chart 1: Monthly Product Revenue vs Gross Profit
    st.subheader("Monthly Product Revenue vs Gross Profit")

    chart1 = filtered_data.set_index("Month")[
        ["Product Revenue", "Gross Profit"]
    ]

    st.line_chart(chart1)

    # Chart 2: Monthly Product Cost Trend
    st.subheader("Monthly Product Cost Trend")

    chart2 = filtered_data.set_index("Month")[["Product Cost"]]

    st.line_chart(chart2)

    # Chart 3: Monthly Gross Profit Trend
    st.subheader("Monthly Gross Profit Trend")

    chart3 = filtered_data.set_index("Month")[["Gross Profit"]]

    st.line_chart(chart3)

    st.caption(
        "January 2026 contains partial-month data and should not be "
        "compared directly with complete months."
    )
