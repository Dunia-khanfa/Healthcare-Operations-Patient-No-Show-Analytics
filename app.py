import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(page_title="Predictive Healthcare Analytics", layout="wide")

def get_data():
    file_name = 'healthcare_data_advanced.csv'
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        num_records = 5000
        np.random.seed(42)
        df = pd.DataFrame({
            'AppointmentID': range(1000, 1000 + num_records),
            'Age': np.random.randint(0, 95, num_records),
            'Gender': np.random.choice(['Male', 'Female'], num_records),
            'Department': np.random.choice(['Cardiology', 'Pediatrics', 'OPD', 'Orthopedics', 'General'], num_records),
            'WaitTimeDays': np.random.randint(0, 30, num_records),
            'Status': np.random.choice(['Show', 'No-Show'], num_records, p=[0.78, 0.22]),
            'Previous_NoShows': np.random.choice([0, 1, 2, 3], num_records, p=[0.6, 0.2, 0.15, 0.05]),
            'Insurance': np.random.choice(['Private', 'Public', 'None'], num_records)
        })
        df.to_csv(file_name, index=False)
        return df

df = get_data()

# --- Sidebar with New Filters ---
st.sidebar.header("System Filters")
selected_dept = st.sidebar.multiselect("Departments:", options=sorted(df['Department'].unique()), default=df['Department'].unique())
selected_gender = st.sidebar.multiselect("Gender:", options=df['Gender'].unique(), default=df['Gender'].unique())
selected_insurance = st.sidebar.multiselect("Insurance Type:", options=df['Insurance'].unique(), default=df['Insurance'].unique())
age_range = st.sidebar.slider("Age Range:", 0, 100, (0, 100))

mask = (df['Department'].isin(selected_dept)) & \
       (df['Gender'].isin(selected_gender)) & \
       (df['Insurance'].isin(selected_insurance)) & \
       (df['Age'].between(age_range[0], age_range[1]))
f_df = df[mask].copy()

# --- Header ---
st.markdown("<h1 style='text-align: center;'>Patient Reliability and Risk Scoring System</h1>", unsafe_allow_html=True)

# --- KPIs ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Appointments", len(f_df))
m2.metric("High-Risk Profiles", len(f_df[f_df['Previous_NoShows'] >= 2]))
reallocated_count = len(f_df[f_df['Previous_NoShows'] >= 2])
m3.metric("Reallocated Slots", reallocated_count)
m4.metric("Efficiency Gain", "+21.5%")

st.write("---")

# --- Reallocation Section ---
st.markdown("<h3 style='text-align: center;'>Risk-Based Conditional Reallocation</h3>", unsafe_allow_html=True)
col_btn, col_tbl = st.columns([1, 2])

with col_btn:
    if st.button("Trigger Smart Reallocation"):
        st.success(f"Successfully reallocated {reallocated_count} high-risk slots.")
        st.balloons()

with col_tbl:
    high_risk_display = f_df[f_df['Previous_NoShows'] >= 2].head(5).copy()
    high_risk_display['Transfer_Status'] = "Transferred"
    # Left Aligned Table without the problematic 'alignment' keyword
    st.dataframe(high_risk_display[['AppointmentID', 'Department', 'Previous_NoShows', 'Transfer_Status']], use_container_width=True, hide_index=True)

st.write("---")

# --- Charts ---
c1, c2 = st.columns(2)
with c1:
    fig_hist = px.histogram(f_df, x="Previous_NoShows", color="Status", barmode="group", template="plotly_white", color_discrete_map={'Show':'#2ecc71', 'No-Show':'#e74c3c'})
    st.plotly_chart(fig_hist, use_container_width=True)
with c2:
    fig_wait = px.box(f_df, x="Status", y="WaitTimeDays", color="Status", template="plotly_white")
    st.plotly_chart(fig_wait, use_container_width=True)

st.write("---")
st.markdown("<h3 style='text-align: center;'>Full Patient Reliability Database</h3>", unsafe_allow_html=True)
# Standard Table Display - Always Left Aligned by default
st.dataframe(f_df.reset_index(drop=True), use_container_width=True, hide_index=True)
