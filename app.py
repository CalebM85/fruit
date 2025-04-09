import streamlit as st
import pandas as pd
import plotly.express as px

# Set up page
st.set_page_config(page_title="Cherry Securitization Trust 2024-1 Dashboard", layout="wide")
st.title("📊 Cherry Securitization Trust 2024-1 Dashboard")
st.markdown("""
A visual breakdown of the pre-sale report to help analyze the collateral pool, structure, and credit enhancement.
""")

# Deal Summary
with st.expander("📄 Deal Summary"):
    st.write("""
    - **Deal Name**: Cherry Securitization Trust 2024-1  
    - **Issue Date**: Expected October 2, 2024  
    - **Total Issuance**: $250,000,000  
    - **Revolving Period**: 24 months (ends Sept 30, 2026 or earlier upon Amortization Event)
    - **Rated Notes**:
        - Class A: $191.8M (A (sf), 27.51% CE)
        - Class B: $19.2M (BBB (sf), 20.16% CE)
        - Class C: $14.9M (BB (sf), 14.46% CE)
        - Class D: $24.2M (B (sf), 5.21% CE)
    - **Initial Overcollateralization**: 4.25%, Target: 6.25%
    - **Excess Spread**: ~11.22%
    - **KBRA Base Case Loss Expectation**: 8.90%
    """)

# Sample data for visuals
promo_vs_nonpromo = pd.DataFrame({
    'Type': ['Promotional (0% APR)', 'Non-Promotional'],
    'Balance ($M)': [109.3, 162.3]
})

vantage_scores = pd.DataFrame({
    'Score Band': ['520-599', '600-659', '660-699', '700+'],
    'Distribution (%)': [2.67, 19.95, 21.59, 55.78]
})

state_concentration = pd.DataFrame({
    'State': ['California', 'Florida', 'Texas', 'New York', 'Arizona'],
    'Balance ($M)': [43.6, 37.5, 36.8, 16.2, 10.3]
})

industries = pd.DataFrame({
    'Industry': ['Dental', 'Medspa', 'Cosmetic Surgery', 'Other'],
    'Balance ($M)': [113.9, 111.3, 44.7, 1.7]
})

# Layout: Filters + Charts
col1, col2 = st.columns(2)

with col1:
    fig1 = px.pie(promo_vs_nonpromo, names='Type', values='Balance ($M)', title='Loan Type Distribution')
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(vantage_scores, x='Score Band', y='Distribution (%)', title='Vantage Score Distribution')
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    fig3 = px.bar(state_concentration, x='State', y='Balance ($M)', title='Top State Concentrations')
    st.plotly_chart(fig3, use_container_width=True)

    fig4 = px.pie(industries, names='Industry', values='Balance ($M)', title='Industry Mix')
    st.plotly_chart(fig4, use_container_width=True)

# Footer
st.markdown("""
---
**Data Source**: KBRA Pre-Sale Report for Cherry Securitization Trust 2024-1 (September 2024)
""")
