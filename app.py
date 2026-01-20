import streamlit as st
import pandas as pd
import plotly.express as px

# 1. PAGE SETUP
st.set_page_config(
    page_title="Aadhaar Sentinel | UIDAI Data Intelligence",
    page_icon="🛡️",
    layout="wide"
)

# 2. UI STYLING (Minimalist & Professional)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Executive Briefing Box */
    .mission-card {
        background-color: #ffffff;
        border: 1px solid #e1e4e8;
        padding: 24px;
        border-radius: 12px;
        border-left: 6px solid #1a73e8;
        margin-bottom: 25px;
    }
    
    .mission-title {
        color: #1a73e8;
        font-weight: 800;
        font-size: 1.2rem;
        margin-bottom: 8px;
    }

    /* Metric Styling */
    [data-testid="stMetricValue"] {
        font-weight: 700;
        color: #1a73e8;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. DATA LOADING
@st.cache_data
def load_data():
    # Ensure this file exists in your GitHub repository
    return pd.read_csv('processed_aadhaar_data.csv')

df = load_data()

# 4. SIDEBAR - CONTROL CENTER (City/District Selection)
with st.sidebar:
    st.markdown("## **Control Center**")
    st.caption("Filter parameters for deep-dive analysis.")
    
    # State Selection
    states = sorted(df['state'].unique())
    selected_state = st.selectbox("Select State", ["All India"] + states)
    
    # District/City Selection (Dynamic based on State)
    if selected_state != "All India":
        districts = sorted(df[df['state'] == selected_state]['district'].unique())
        selected_district = st.selectbox("Select District/City", ["All Districts"] + districts)
    else:
        selected_district = "All Districts"
    
    st.divider()
    st.caption("UIDAI Hackathon 2026 | Analytical Framework v2.0")

# 5. DATA FILTERING LOGIC
filtered_df = df.copy()
if selected_state != "All India":
    filtered_df = filtered_df[filtered_df['state'] == selected_state]
if selected_district != "All Districts":
    filtered_df = filtered_df[filtered_df['district'] == selected_district]

# 6. HEADER & STRATEGIC MISSION
st.title("🛡️ Aadhaar Sentinel")
st.markdown(f"""
    <div class="mission-card">
        <div class="mission-title">EXECUTIVE STRATEGIC BRIEFING</div>
        <p style="color: #444; line-height: 1.6;">
            <strong>Objective:</strong> To maintain the integrity of India's digital identity backbone by identifying 
            <strong>exclusion vulnerabilities</strong>. This framework monitors the delta between historical child enrolments 
            and mandatory biometric refreshes, ensuring continuous welfare access for <strong>{selected_district if selected_district != 'All Districts' else 'Nationwide'}</strong> clusters.
        </p>
    </div>
    """, unsafe_allow_html=True)

# 7. PERFORMANCE METRICS
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Districts Analyzed", len(filtered_df))
with m2:
    updates = int(filtered_df['total_updates'].sum())
    st.metric("Service Volume", f"{updates:,}")
with m3:
    risk_score = round(filtered_df['vulnerability_score'].mean(), 2)
    st.metric("Maintenance Index", risk_score)
with m4:
    # Logic for System Health
    health = "Stable" if risk_score > 100 else "Critical"
    st.metric("System Health", health)

st.divider()

# 8. CORE ANALYTICS
tab1, tab2 = st.tabs(["🎯 Exclusion Analytics", "📁 District Data Explorer"])

with tab1:
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.markdown("### **Vulnerability Mapping**")
        fig = px.scatter(
            filtered_df, x="total_enrol", y="total_updates", size="vulnerability_score",
            color="vulnerability_score", hover_name="district",
            log_x=True, log_y=True,
            color_continuous_scale='RdBu', # Professional Red-Blue scale
            template="plotly_white"
        )
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=30))
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("### **Top Priority Nodes**")
        # Showing top 5 districts in current filter needing attention
        top_5 = filtered_df.sort_values('vulnerability_score').head(5)
        st.dataframe(top_5[['district', 'vulnerability_score']], hide_index=True, use_container_width=True)
        st.caption("Districts with the lowest maintenance ratios.")

with tab2:
    st.markdown("### **Master Records**")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# 9. AI PREDICTIVE RECOMMENDATION (The X-Factor)
st.divider()
st.subheader("🤖 Predictive Governance Action")

if not filtered_df.empty:
    priority = filtered_df.sort_values('vulnerability_score').iloc[0]
    st.warning(f"**High Priority:** District **{priority['district']}** is identified as a primary exclusion risk.")
    st.info(f"**Recommended Response:** Deploy 2 Mobile Aadhaar Units to this district to facilitate Mandatory Biometric Updates (MBU) for the 5-15 age cohort.")
else:
    st.error("No data available for the selected filters.")
