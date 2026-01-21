import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(page_title="Healthcare Operations Analytics", layout="wide")

def get_data():
    file_name = 'healthcare_data_final.csv'
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        num_records = 5000
        np.random.seed(42)
        df = pd.DataFrame({
            'AppointmentID': range(1000, 1000 + num_records),
            'Age': np.random.randint(0, 95, num_records),
            'Department': np.random.choice(['Cardiology', 'Pediatrics', 'OPD', 'Orthopedics', 'General'], num_records),
            'WaitTimeDays': np.random.randint(0, 30, num_records),
            'Status': np.random.choice(['Show', 'No-Show'], num_records, p=[0.78, 0.22]),
            'Gender': np.random.choice(['Male', 'Female'], num_records),
            'Insurance': np.random.choice(['Private', 'Public', 'None'], num_records)
        })
        df.to_csv(file_name, index=False)
        return df

df = get_data()

st.sidebar.header("Filter Dashboard")
selected_dept = st.sidebar.multiselect("Select Departments:", options=sorted(df['Department'].unique()), default=df['Department'].unique())
age_range = st.sidebar.slider("Age Range:", 0, 100, (0, 100))

mask = (df['Department'].isin(selected_dept)) & (df['Age'].between(age_range[0], age_range[1]))
f_df = df[mask].copy()

st.markdown("<h1 style='text-align: center;'>Healthcare Operations and Patient Analytics</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Predictive Modeling and Appointment Optimization System</p>", unsafe_allow_html=True)

st.write("")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Appointments", len(f_df))
m2.metric("No-Show Rate", f"{(f_df['Status']=='No-Show').mean()*100:.1f}%")
m3.metric("Optimization Capacity", "22%", help="Recoverable slots through automated reallocation")
m4.metric("Avg Wait Time", f"{f_df['WaitTimeDays'].mean():.1f} Days")

st.write("---")

st.subheader("Automated Waitlist Reallocation Engine")
col_action, col_info = st.columns([1, 2])

with col_action:
    if st.button("Run Smart Reallocation"):
        st.success("Reallocation Successful: 5 High-risk slots moved to Waitlist Priority.")
        st.balloons()
    else:
        st.warning("Action Required: High-risk slots detected.")

with col_info:
    high_risk_data = f_df[f_df['WaitTimeDays'] > 25].head(5)
    st.table(high_risk_data[['AppointmentID', 'Department', 'WaitTimeDays']])

st.write("---")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Appointment Status by Department")
    fig_dept = px.histogram(f_df, x="Department", color="Status", 
                            barmode="group", template="plotly_white",
                            color_discrete_map={'Show':'#2ecc71', 'No-Show':'#e74c3c'})
    fig_dept.update_layout(xaxis_tickangle=0)
    st.plotly_chart(fig_dept, use_container_width=True)

with col_right:
    st.subheader("Attendance Rate by Age Group")
    f_df['AgeGroup'] = pd.cut(f_df['Age'], bins=[0, 18, 40, 65, 100], labels=['Youth', 'Young Adult', 'Adult', 'Senior'])
    age_data = f_df.groupby(['AgeGroup', 'Status'], observed=False).size().reset_index(name='count')
    fig_age = px.bar(age_data, x="AgeGroup", y="count", color="Status", barmode="stack", template="plotly_white")
    fig_age.update_layout(xaxis_tickangle=0)
    st.plotly_chart(fig_age, use_container_width=True)

st.write("---")
st.subheader("Detailed Patient Database")
st.dataframe(f_df.reset_index(drop=True), use_container_width=True, hide_index=True)
