import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="Aadhaar Social Pulse | UIDAI 2026", layout="wide")

# 2. Premium Styling (Custom CSS for a modern "Command Center" feel)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    /* Styling the Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 700;
        color: #003366;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-left: 5px solid #003366;
    }
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 5px 5px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #003366 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Data Loading Function
@st.cache_data
def load_data():
    # This must match the filename generated in VS Code
    df = pd.read_csv('processed_aadhaar_data.csv')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️ Data file not found. Please ensure 'processed_aadhaar_data.csv' is uploaded to GitHub.")
    st.stop()

# 4. Sidebar Control Panel
st.sidebar.header("🕹️ Control Center")
st.sidebar.markdown("Use these filters to drill down into regional data.")
selected_state = st.sidebar.selectbox("Filter by State", ["All India"] + list(df['state'].unique()))

if selected_state != "All India":
    display_df = df[df['state'] == selected_state]
else:
    display_df = df

# 5. Header Section
st.title("🇮🇳 Aadhaar Societal Trends & Inclusion Dashboard")
st.markdown("#### *Leveraging Data for Universal Identity Maintenance*")
st.divider()

# 6. Strategic KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Districts Monitored", value=len(display_df))
with col2:
    total_upd = int(display_df['total_updates'].sum())
    st.metric(label="Lifecycle Updates", value=f"{total_upd:,}")
with col3:
    # Logic: Lower vulnerability score means higher risk of exclusion
    risk_zones = len(display_df[display_df['vulnerability_score'] < 100]) 
    st.metric(label="Critical Risk Zones", value=risk_zones, delta="Needs Attention", delta_color="inverse")
with col4:
    avg_score = f"{display_df['vulnerability_score'].mean():.1f}"
    st.metric(label="Avg. Maintenance Index", value=avg_score)

st.divider()

# 7. Strategic Analysis Tabs
tab1, tab2, tab3 = st.tabs(["📍 Exclusion Risk Analysis", "🚀 Migration & Growth", "📁 Raw Data Explorer"])

with tab1:
    st.subheader("Predicting Mandatory Biometric Update (MBU) Gaps")
    st.markdown("""
    This visualization identifies districts where **New Enrolments** are high but **Updates** are low. 
    A larger bubble indicates a higher 'Exclusion Risk' where residents may lose access to welfare benefits.
    """)
    
    fig_risk = px.scatter(display_df, 
                         x="total_enrol", 
                         y="total_updates", 
                         size="vulnerability_score", 
                         color="state" if selected_state == "All India" else "district",
                         hover_name="district",
                         log_x=True, log_y=True,
                         title="Correlation: Enrolment Cohorts vs. Update Compliance",
                         template="plotly_white",
                         color_discrete_sequence=px.colors.qualitative.Bold)
    
    st.plotly_chart(fig_risk, use_container_width=True)


    # ... (all your existing scatter plot code is here) ...
    
    # ADD THE X-FACTOR HERE:
    st.divider()
    st.subheader("🤖 AI-Driven Strategic Recommendation")
    
    # This logic automatically finds the district with the lowest score
    priority_district = display_df.sort_values('vulnerability_score').iloc[0]
    
    st.warning(f"**Action Required:** High exclusion risk detected in **{priority_district['district']}**, {priority_district['state']}.")
    st.info(f"""
    **Recommended Response for {priority_district['district']}:**
    * **Resource Allocation:** Deploy 2 Mobile Aadhaar Units to this district immediately.
    * **Target Demographic:** Prioritize residents aged 5-17 for Mandatory Biometric Updates.
    * **Inclusion Goal:** Aim to reduce the 'Exclusion Delta' by 15% within the next quarter.
    """)

with tab2:
    st.subheader("Tracking Internal Migration Hubs")
    st.write("Districts with abnormally high update-to-enrolment ratios signify economic destination zones.")
    
    col_a, col_b = st.columns([1, 2])
    
    with col_a:
        top_mig = display_df.sort_values('vulnerability_score', ascending=False).head(12)
        st.write("**Top 12 Destination Districts**")
        st.table(top_mig[['district', 'vulnerability_score']].reset_index(drop=True))
    
    with col_b:
        fig_mig = px.bar(top_mig, 
                        x='vulnerability_score', 
                        y='district', 
                        orientation='h',
                        color='vulnerability_score',
                        color_continuous_scale='Blues',
                        title="Update Intensity Index (Migration Proxies)")
        st.plotly_chart(fig_mig, use_container_width=True)

with tab3:
    st.subheader("Granular Data Analysis")
    st.write("Search and filter the processed master dataset.")
    st.dataframe(display_df.style.highlight_max(axis=0, subset=['total_updates']), use_container_width=True)
    
    # Premium Feature: Download Button
    csv = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Processed Insights (CSV)",
        data=csv,
        file_name='aadhaar_processed_data.csv',
        mime='text/csv',
    )

# 8. Professional Footer
st.divider()
st.caption("Official Submission for UIDAI Data Hackathon 2026 | Built with Streamlit & Plotly")
