

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="E-Commerce Customer Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("E-Commerce Customer Analytics")
st.caption("Interactive public portfolio demo | Python • SQL • dbt • Power BI • Machine Learning")

# Project KPIs
st.header("Executive Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Order Revenue", "$63.46M")
col2.metric("Gross Product Profit", "$29.60M")
col3.metric("Product Margin", "50.40%")
col4.metric("Repeat Purchase Rate", "95.8%")

st.divider()

# Navigation
tab1, tab2, tab3, tab4 = st.tabs([
    "Executive Overview",
    "Product Performance",
    "Customer Analytics",
    "ML & AI Insights"
])

with tab1:
    st.subheader("Business Overview")

    st.write("""
    This project analyzes e-commerce customer behavior, purchasing patterns,
    product profitability and revenue performance using an end-to-end
    analytics and machine learning workflow.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Customer Acquisition Channels")

        channels = pd.DataFrame({
            "Channel": [
                "Organic", "Paid Search", "Paid Social",
                "Referral", "Affiliate"
            ],
            "Customers": [6117, 4994, 3932, 2920, 2037]
        }).set_index("Channel")

        st.bar_chart(channels)

    with col2:
        st.subheader("Customer Behavior Segments")

        segments = pd.DataFrame({
            "Segment": [
                "High Value Frequent", "Regular", "At Risk"
            ],
            "Customers": [6418, 9955, 3477]
        }).set_index("Segment")

        st.bar_chart(segments)


with tab2:
    st.subheader("Product Performance")

    st.metric("Total Gross Product Profit", "$29.60M")
    st.metric("Overall Product Margin", "50.40%")

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

    customer_types = pd.DataFrame({
        "Customer Type": [
            "Consumer", "Small Business", "Enterprise"
        ],
        "Customers": [16407, 2989, 604]
    }).set_index("Customer Type")

    st.write("Customer types")
    st.bar_chart(customer_types)

    st.subheader("K-Means Customer Segmentation")

    segment_details = pd.DataFrame({
        "Behavior Segment": [
            "High Value Frequent", "Regular", "At Risk"
        ],
        "Customers": [6418, 9955, 3477],
        "Average Orders": [7.30, 4.04, 2.88],
        "Average Spend ($)": [5191.13, 2394.89, 1812.12]
    })

    st.dataframe(segment_details, hide_index=True, use_container_width=True)

    st.caption(
        "Customer types and behavioral segments are two different "
        "classifications."
    )

with tab4:
    st.subheader("Machine Learning & AI Insights")

    st.markdown("**Machine Learning techniques implemented**")

    st.markdown("""
    - K-Means clustering for customer segmentation
    - Classification for repeat purchase prediction
    - Monthly revenue forecasting
    - Hyperparameter tuning and model evaluation
    """)

    st.warning(
        "The repeat-purchase prediction model achieved a ROC-AUC "
        "of approximately 0.50, indicating weak predictive performance. "
        "This limitation is reported transparently."
    )

    st.subheader("Business Question Explorer")

    question = st.selectbox(
        "Choose a business question",
        [
            "Which product category generated the highest gross profit?",
            "Which customer type had the highest average spending?",
            "Which month recorded the highest order revenue?",
            "What is the overall product profit margin?"
        ]
    )

    answers = {
        "Which product category generated the highest gross profit?":
            "Electronics recorded the highest total gross profit.",

        "Which customer type had the highest average spending?":
            "Consumer customers had the highest average spending.",

        "Which month recorded the highest order revenue?":
            "March 2023 recorded the highest monthly order revenue: $1,906,024.15.",

        "What is the overall product profit margin?":
            "The overall product profit margin was 50.40%."
    }

    if st.button("Explore Answer"):
        st.success(answers[question])

st.divider()

st.caption(
    "Portfolio demonstration using precomputed project findings. "
    "This public demo does not connect to the local PostgreSQL database "
    "or run the local Ollama model."
)
