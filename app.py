import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(page_title="HMO Resource Optimization", layout="wide")

st.markdown("""
    <style>
    .block-container {
        padding-top: 0.2rem;
        padding-bottom: 0rem;
    }
    h1 {
        margin-top: -3.5rem;
        font-size: 2.5rem;
        color: #1E1E1E;
    }
    </style>
    """, unsafe_allow_html=True)

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

st.markdown("<h1 style='text-align: center;'>HMO Resource Optimization: Predictive Patient Reliability Engine</h1>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Appointments", len(f_df))
high_risk_df = f_df[f_df['Previous_NoShows'] >= 2]
m2.metric("High-Risk Profiles", len(high_risk_df))
efficiency = (len(high_risk_df) / len(f_df) * 100) if len(f_df) > 0 else 0
m3.metric("Ready for Action", len(high_risk_df))
m4.metric("Potential Efficiency", f"+{efficiency:.1f}%")

st.write("---")

st.markdown("<h3 style='text-align: center;'>Risk Flagging for HMO Review</h3>", unsafe_allow_html=True)
c_act, c_tbl = st.columns([1, 2])

with c_act:
    if st.button("Flag for Reallocation"):
        st.success(f"Flagged {len(high_risk_df)} slots.")
        st.balloons()

with c_tbl:
    risk_display = high_risk_df[['AppointmentID', 'Department', 'Previous_NoShows', 'WaitTimeDays']].head(10).astype(str)
    st.dataframe(risk_display, use_container_width=True, hide_index=True)

st.write("---")

st.markdown("<h3 style='text-align: center;'>HMO Operational Risk Heatmap</h3>", unsafe_allow_html=True)
f_df['Age_Bin'] = pd.cut(f_df['Age'], bins=[0, 20, 40, 60, 80, 100], labels=['0-20', '21-40', '41-60', '61-80', '81+'])
heat_data = f_df[f_df['Status'] == 'No-Show'].groupby(['Department', 'Age_Bin'], observed=False).size().reset_index(name='NoShows')
fig_heat = px.density_heatmap(heat_data, x='Age_Bin', y='Department', z='NoShows', color_continuous_scale='Reds', template='plotly_white')
st.plotly_chart(fig_heat, use_container_width=True)

st.write("---")

st.markdown("<h3 style='text-align: center;'>Full Patient Reliability Database</h3>", unsafe_allow_html=True)
st.dataframe(f_df.reset_index(drop=True).astype(str), use_container_width=True, hide_index=True)
