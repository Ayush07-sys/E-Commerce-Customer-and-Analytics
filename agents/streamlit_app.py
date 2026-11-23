import pandas as pd
import streamlit as st
from getpass import getpass

from agents.ai_business_analyst import (
    generate_sql,
    validate_sql,
    execute_sql,
    explain_results
)

st.set_page_config(
    page_title="AI E-Commerce Business Analyst",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI E-Commerce Business Analyst")
st.caption("Ask questions about customers, products, revenue and profitability.")

st.divider()

# Database password
password = st.text_input(
    "PostgreSQL ai_analyst password",
    type="password"
)

# Business question
question = st.text_area(
    "Ask your business question",
    placeholder="Example: Which product category generates the highest gross profit?"
)

if st.button("Analyze", type="primary"):
    if not password or not question.strip():
        st.warning("Please enter your database password and business question.")
    else:
        try:
            with st.spinner("Generating SQL using Qwen..."):
                generated_sql = generate_sql(question)

            st.subheader("1. Generated SQL")
            st.code(generated_sql, language="sql")

            with st.spinner("Validating SQL..."):
                validated_sql = validate_sql(generated_sql)

            st.success("SQL validation successful!")

            with st.spinner("Executing query in PostgreSQL..."):
                results = execute_sql(validated_sql, password)

            st.subheader("2. Database Results")

            if results:
                results_df = pd.DataFrame(results)
                st.dataframe(results_df, use_container_width=True)
            else:
                st.info("No records found.")

            with st.spinner("Generating business insights..."):
                answer = explain_results(
                    question,
                    validated_sql,
                    results
                )

            st.subheader("3. AI Business Insights")
            st.markdown(answer)

        except Exception as error:
            st.error(f"Application error: {error}")
