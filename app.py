import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

# Data Definitions
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

merchant_concentration = pd.DataFrame({
    'Merchant': [f'Merchant {i+1}' for i in range(10)],
    'Balance ($M)': [16.1, 5.3, 2.0, 1.8, 1.4, 1.3, 1.25, 1.18, 1.02, 0.98]
})

cashflow_waterfall = go.Figure(go.Waterfall(
    name="Cash Flow Structure",
    orientation="v",
    measure=["relative", "relative", "relative", "relative", "total"],
    x=["Excess Spread", "Reserve Fund", "Subordination", "Overcollateralization", "Total Credit Enhancement"],
    textposition="outside",
    y=[11.22, 1.0, 27.51, 4.25, 43.98],
    connector={"line": {"color": "rgb(63, 63, 63)"}}
))
cashflow_waterfall.update_layout(title="📉 Credit Enhancement Waterfall (Class A)", showlegend=False)

# Interactivity: Filters
with st.sidebar:
    st.header("🔍 Filters")
    state_filter = st.multiselect("Select States", options=state_concentration['State'].unique(), default=state_concentration['State'].unique())
    score_filter = st.multiselect("Select Credit Score Bands", options=vantage_scores['Score Band'].unique(), default=vantage_scores['Score Band'].unique())
    industry_filter = st.multiselect("Select Industries", options=industries['Industry'].unique(), default=industries['Industry'].unique())
    loan_type_filter = st.multiselect("Select Loan Types", options=promo_vs_nonpromo['Type'].unique(), default=promo_vs_nonpromo['Type'].unique())

# Apply filters
filtered_states = state_concentration[state_concentration['State'].isin(state_filter)]
filtered_scores = vantage_scores[vantage_scores['Score Band'].isin(score_filter)]
filtered_industries = industries[industries['Industry'].isin(industry_filter)]
filtered_loans = promo_vs_nonpromo[promo_vs_nonpromo['Type'].isin(loan_type_filter)]

# Layout: Charts
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(px.pie(filtered_loans, names='Type', values='Balance ($M)', title='Loan Type Distribution'), use_container_width=True)
    st.plotly_chart(px.bar(filtered_scores, x='Score Band', y='Distribution (%)', title='Filtered Vantage Score Distribution'), use_container_width=True)

with col2:
    st.plotly_chart(px.bar(filtered_states, x='State', y='Balance ($M)', title='Filtered Top State Concentrations'), use_container_width=True)
    st.plotly_chart(px.pie(filtered_industries, names='Industry', values='Balance ($M)', title='Industry Mix'), use_container_width=True)

# New row
col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(px.bar(merchant_concentration, x='Merchant', y='Balance ($M)', title='Top 10 Merchant Concentrations'), use_container_width=True)

with col4:
    st.plotly_chart(cashflow_waterfall, use_container_width=True)

# Export
st.sidebar.header("📥 Export")
export_data = {
    'States': filtered_states,
    'Scores': filtered_scores,
    'Industries': filtered_industries,
    'Loan Types': filtered_loans
}
selected_export = st.sidebar.selectbox("Choose data to export", list(export_data.keys()))

csv = export_data[selected_export].to_csv(index=False).encode('utf-8')
st.sidebar.download_button("Download CSV", csv, f"{selected_export.lower().replace(' ', '_')}_data.csv", "text/csv")

# Footer
st.markdown("""
---
**Data Source**: KBRA Pre-Sale Report for Cherry Securitization Trust 2024-1 (September 2024)
""")
