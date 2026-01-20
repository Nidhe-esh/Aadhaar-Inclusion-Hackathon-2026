import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Aadhaar Social Pulse", layout="wide")
st.title("🇮🇳 Aadhaar Societal Trends & Inclusion Dashboard")
st.markdown("Analysis of Enrolment and Update patterns for the UIDAI Hackathon 2026.")

# Load the result from our analysis
df = pd.read_csv('processed_aadhaar_data.csv')

# Metric Cards
col1, col2, col3 = st.columns(3)
col1.metric("Total Districts Analyzed", len(df))
col2.metric("High Migration Hubs", len(df[df['vulnerability_score'] > 2000]))
col3.metric("Critical Exclusion Zones", len(df[df['vulnerability_score'] < 500]))

# Map/Chart
st.subheader("Regional Vulnerability Map")
fig = px.scatter(df, x="total_enrol", y="total_updates", 
                 color="state", size="vulnerability_score",
                 hover_name="district", log_x=True, log_y=True)
st.plotly_chart(fig, use_container_width=True)

st.write("Created by [Your Name] for UIDAI Hackathon 2026")
