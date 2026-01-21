import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(page_title="HMO Resource Optimization", layout="wide")

st.markdown("""
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    h1 {
        margin-top: -1rem;
        margin-bottom: 2rem;
        font-size: 2.8rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        font-weight: bold;
        background-color: #f8f9fb;
        border: 1px solid #d1d5db;
    }
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

if 'processed_count' not in st.session_state:
    st.session_state.processed_count = 0

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

high_risk_total = f_df[f_df['Previous_NoShows'] >= 2]
total_risks = len(high_risk_total)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Appointments", len(f_df))
m2.metric("High-Risk Profiles", total_risks)
m3.metric("Actioned by HMO", st.session_state.processed_count)
eff_gain = (st.session_state.processed_count / len(f_df) * 100) if len(f_df) > 0 else 0
m4.metric("Efficiency Gain", f"+{eff_gain:.1f}%")

st.write("")
st.write("---")
st.write("")

st.markdown("<h3 style='text-align: center; margin-bottom: 1.5rem;'>Risk Flagging & Case Management</h3>", unsafe_allow_html=True)

# שימוש בעמודות עם יחס מרווח יותר למניעת דחיסות
col_btn, spacer, col_tbl = st.columns([1.2, 0.3, 3.5])

with col_btn:
    st.write("Process the next batch for review:")
    if st.button("Flag Next 25 Cases"):
        if st.session_state.processed_count < total_risks:
            st.session_state.processed_count += min(25, total_risks - st.session_state.processed_count)
            st.rerun()
    
    st.write("")
    if st.session_state.processed_count > 0:
        st.info(f"Currently monitoring {st.session_state.processed_count} flagged slots.")
    else:
        st.warning("No cases flagged for action yet.")

with col_tbl:
    risk_display = high_risk_total.head(10).astype(str)
    st.dataframe(risk_display[['AppointmentID', 'Department', 'Previous_NoShows', 'WaitTimeDays']], use_container_width=True, hide_index=True)

st.write("")
st.write("---")
st.write("")

st.markdown("<h3 style='text-align: center; margin-bottom: 1rem;'>HMO Operational Risk Heatmap</h3>", unsafe_allow_html=True)
f_df['Age_Bin'] = pd.cut(f_df['Age'], bins=[0, 20, 40, 60, 80, 100], labels=['0-20', '21-40', '41-60', '61-80', '81+'])
heat_data = f_df[f_df['Status'] == 'No-Show'].groupby(['Department', 'Age_Bin'], observed=False).size().reset_index(name='NoShows')
fig_heat = px.density_heatmap(heat_data, x='Age_Bin', y='Department', z='NoShows', color_continuous_scale='Reds', template='plotly_white')
fig_heat.update_layout(margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig_heat, use_container_width=True)

st.write("---")

st.markdown("<h3 style='text-align: center;'>Full Patient Reliability Database</h3>", unsafe_allow_html=True)
st.dataframe(f_df.reset_index(drop=True).astype(str), use_container_width=True, hide_index=True)
