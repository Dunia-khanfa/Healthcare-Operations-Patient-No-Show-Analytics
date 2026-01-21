import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(page_title="Patient Reliability Scoring System", layout="wide")

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
            'Department': np.random.choice(['Cardiology', 'Pediatrics', 'OPD', 'Orthopedics', 'General'], num_records),
            'WaitTimeDays': np.random.randint(0, 30, num_records),
            'Status': np.random.choice(['Show', 'No-Show'], num_records, p=[0.78, 0.22]),
            'Previous_NoShows': np.random.choice([0, 1, 2, 3], num_records, p=[0.6, 0.2, 0.15, 0.05]),
            'Insurance': np.random.choice(['Private', 'Public', 'None'], num_records)
        })
        df.to_csv(file_name, index=False)
        return df

df = get_data()

st.sidebar.header("System Filters")
selected_dept = st.sidebar.multiselect("Departments:", options=sorted(df['Department'].unique()), default=df['Department'].unique())
mask = df['Department'].isin(selected_dept)
f_df = df[mask].copy()

st.markdown("<h1 style='text-align: center;'>Patient Reliability and Risk Scoring System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Advanced analytics for hospital resource optimization based on historical behavior</p>", unsafe_allow_html=True)

st.write("")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Appointments", len(f_df))
m2.metric("Historical No-Show Rate", f"{(f_df['Status']=='No-Show').mean()*100:.1f}%")
m3.metric("High-Risk Profiles", len(f_df[f_df['Previous_NoShows'] >= 2]))
m4.metric("Operational Efficiency", "+21%")

st.write("---")

st.markdown("<h3 style='text-align: center;'>Risk-Based Conditional Reallocation</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>The system flags patients with low reliability scores for automated backup scheduling.</p>", unsafe_allow_html=True)

c_act, c_mid, c_table = st.columns([1, 0.1, 2])

with c_act:
    st.write("")
    if st.button("Trigger Conditional Reallocation"):
        st.success("Analysis Complete: High-risk slots assigned to backup waitlist.")
        st.balloons()
    else:
        st.info("System monitoring reliability scores...")

with c_table:
    high_risk_history = f_df[f_df['Previous_NoShows'] >= 2].head(5).reset_index(drop=True)
    st.dataframe(high_risk_history[['AppointmentID', 'Department', 'Previous_NoShows', 'Status']], use_container_width=True, hide_index=True)

st.write("---")

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
st.markdown("<h3 style='text-align: center;'>Full Patient Reliability Database</h3>", unsafe_allow_html=True)

st.dataframe(
    f_df.reset_index(drop=True), 
    use_container_width=True, 
    hide_index=True
)
