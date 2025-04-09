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

# Time-based performance trends (static pool example data)
static_pool = pd.DataFrame({
    'Month': ["Month 1", "Month 2", "Month 3", "Month 4", "Month 5", "Month 6"],
    'Cumulative Net Loss (%)': [0.2, 0.5, 0.9, 1.3, 1.7, 2.1],
    '30+ DQ Rate (%)': [0.5, 0.8, 1.1, 1.5, 1.6, 1.8]
})

# Line chart for losses and delinquencies
loss_fig = px.line(static_pool, x='Month', y='Cumulative Net Loss (%)', markers=True, title="📉 Static Pool Cumulative Net Loss")
dq_fig = px.line(static_pool, x='Month', y='30+ DQ Rate (%)', markers=True, title="📊 Static Pool 30+ Day Delinquency Rate")

# Render charts
col_a, col_b = st.columns(2)
with col_a:
    st.plotly_chart(loss_fig, use_container_width=True)
with col_b:
    st.plotly_chart(dq_fig, use_container_width=True)
    
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
    'Balance ($M)': [43.6, 37.5, 36.8, 16.2, 10.3],
    'Avg Vantage Score': [705, 695, 690, 700, 685],
    'Avg APR (%)': [9.5, 10.2, 10.0, 9.8, 10.5]
})

industries = pd.DataFrame({
    'Industry': ['Dental', 'Medspa', 'Cosmetic Surgery', 'Other'],
    'Balance ($M)': [113.9, 111.3, 44.7, 1.7]
})

merchant_concentration = pd.DataFrame({
    'Merchant': [f'Merchant {i+1}' for i in range(10)],
    'Balance ($M)': [16.1, 5.3, 2.0, 1.8, 1.4, 1.3, 1.25, 1.18, 1.02, 0.98]
})

loan_terms = pd.DataFrame({
    'Term (Months)': ['3', '6', '12', '18', '24', '36', '48', '60'],
    'Balance ($M)': [3.6, 21.5, 59.5, 31.6, 95.6, 16.8, 9.1, 33.9]
})

loan_buckets = pd.DataFrame({
    'Loan Size Bucket': [
        '$0–499', '$500–999', '$1,000–1,499', '$1,500–1,999',
        '$2,000–2,499', '$2,500–2,999', '$3,000–3,499', '$3,500–3,999',
        '$4,000–4,999', '$5,000–7,499', '$7,500–9,999', '$10,000–14,999', '$15,000+'
    ],
    'Balance ($M)': [7.4, 18.2, 19.7, 21.5, 20.0, 18.5, 15.0, 14.2, 30.1, 39.0, 24.8, 20.9, 22.4]
})

state_concentration['State Code'] = ['CA', 'FL', 'TX', 'NY', 'AZ']

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

# Layout: Charts
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(px.pie(promo_vs_nonpromo, names='Type', values='Balance ($M)', title='Loan Type Distribution'), use_container_width=True)
    st.plotly_chart(px.bar(vantage_scores, x='Score Band', y='Distribution (%)', title='Vantage Score Distribution'), use_container_width=True)

with col2:
    st.plotly_chart(px.bar(state_concentration, x='State', y='Balance ($M)', title='Top State Concentrations'), use_container_width=True)
    st.plotly_chart(px.pie(industries, names='Industry', values='Balance ($M)', title='Industry Mix'), use_container_width=True)

# New row
col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(px.bar(merchant_concentration, x='Merchant', y='Balance ($M)', title='Top 10 Merchant Concentrations'), use_container_width=True)
    st.plotly_chart(px.bar(loan_terms, x='Term (Months)', y='Balance ($M)', title='Receivable Term Distribution'), use_container_width=True)

with col4:
    st.plotly_chart(cashflow_waterfall, use_container_width=True)
    st.plotly_chart(px.bar(loan_buckets, x='Loan Size Bucket', y='Balance ($M)', title='Loan Size Buckets Distribution'), use_container_width=True)

# Geo Heatmaps
st.markdown("### 🌍 Geographic Heatmaps")
geo_fig_balance = px.choropleth(
    state_concentration,
    locations="State Code",
    locationmode="USA-states",
    color="Balance ($M)",
    color_continuous_scale="Blues",
    scope="usa",
    labels={"Balance ($M)": "Loan Balance ($M)"},
    title="Loan Concentration by State"
)
geo_fig_score = px.choropleth(
    state_concentration,
    locations="State Code",
    locationmode="USA-states",
    color="Avg Vantage Score",
    color_continuous_scale="Greens",
    scope="usa",
    title="Average Vantage Score by State"
)
geo_fig_apr = px.choropleth(
    state_concentration,
    locations="State Code",
    locationmode="USA-states",
    color="Avg APR (%)",
    color_continuous_scale="Reds",
    scope="usa",
    title="Average APR by State"
)

st.plotly_chart(geo_fig_balance, use_container_width=True)
st.plotly_chart(geo_fig_score, use_container_width=True)
st.plotly_chart(geo_fig_apr, use_container_width=True)

# Export
st.sidebar.header("📥 Export")
export_data = {
    'States': state_concentration,
    'Scores': vantage_scores,
    'Industries': industries,
    'Loan Types': promo_vs_nonpromo,
    'Terms': loan_terms,
    'Loan Buckets': loan_buckets
}
selected_export = st.sidebar.selectbox("Choose data to export", list(export_data.keys()))

csv = export_data[selected_export].to_csv(index=False).encode('utf-8')
st.sidebar.download_button("Download CSV", csv, f"{selected_export.lower().replace(' ', '_')}_data.csv", "text/csv")

# Footer
st.markdown("""
---
**Data Source**: KBRA Pre-Sale Report for Cherry Securitization Trust 2024-1 (September 2024)
""")
