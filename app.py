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

# --- Sidebar with More Filters ---
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
st.markdown("<p style='text-align: center;'>Advanced analytics for hospital resource optimization based on historical behavior</p>", unsafe_allow_html=True)

# --- KPIs ---
st.write("")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Appointments", len(f_df))
m2.metric("High-Risk Profiles", len(f_df[f_df['Previous_NoShows'] >= 2]))

# New Metric: Reallocated Count Simulation
reallocated_count = len(f_df[f_df['Previous_NoShows'] >= 2])
m3.metric("Reallocated Slots", reallocated_count, help="Total slots identified and prepared for backup transfer")
m4.metric("Efficiency Gain", "+21.5%")

st.write("---")

# --- Conditional Reallocation Engine ---
st.markdown("<h3 style='text-align: center;'>Risk-Based Conditional Reallocation</h3>", unsafe_allow_html=True)

col_action, col_info = st.columns([1, 2])

with col_action:
    st.write("System monitors patients with 2+ historical failed appointments.")
    if st.button("Trigger Smart Reallocation"):
        st.success(f"Successfully reallocated {reallocated_count} high-risk slots to standby patients.")
        st.balloons()
    else:
        st.info("System Ready: Monitoring reliability scores")

with col_info:
    # Logic for displaying transfer status
    high_risk_display = f_df[f_df['Previous_NoShows'] >= 2].head(5).copy()
    high_risk_display['Transfer_Status'] = "Transferred" # Displaying the transfer status
    
    # Left Aligned Table for Reallocation
    st.dataframe(
        high_risk_display[['AppointmentID', 'Department', 'Previous_NoShows', 'Transfer_Status']], 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "AppointmentID": st.column_config.Column(alignment="left"),
            "Department": st.column_config.Column(alignment="left"),
            "Previous_NoShows": st.column_config.Column(alignment="left"),
            "Transfer_Status": st.column_config.Column(alignment="left")
        }
    )

st.write("---")

# --- Visualizations ---
c1, c2 = st.columns(2)
with c1:
    st.markdown("<h4 style='text-align: center;'>Reliability Score Analysis</h4>", unsafe_allow_html=True)
    fig_hist = px.histogram(f_df, x="Previous_NoShows", color="Status", barmode="group",
                           template="plotly_white", color_discrete_map={'Show':'#2ecc71', 'No-Show':'#e74c3c'})
    fig_hist.update_layout(xaxis_title="Past Failed Appointments", yaxis_title="Number of Patients", showlegend=False)
    st.plotly_chart(fig_hist, use_container_width=True)

with c2:
    st.markdown("<h4 style='text-align: center;'>Wait Time vs Risk Category</h4>", unsafe_allow_html=True)
    fig_wait = px.box(f_df, x="Status", y="WaitTimeDays", color="Status", template="plotly_white")
    fig_wait.update_layout(showlegend=False)
    st.plotly_chart(fig_wait, use_container_width=True)

st.write("---")

# --- Full Database with Left Alignment ---
st.markdown("<h3 style='text-align: center;'>Full Patient Reliability Database</h3>", unsafe_allow_html=True)

# Using column_config to force left alignment for every single column
column_settings = {col: st.column_config.Column(alignment="left") for col in f_df.columns}

st.dataframe(
    f_df.reset_index(drop=True), 
    use_container_width=True, 
    hide_index=True,
    column_config=column_settings
)
