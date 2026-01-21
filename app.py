import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(page_title="HMO Optimization", layout="wide")

st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-left: 10%;
        padding-right: 10%;
    }
    h1 {
        margin-top: -1.5rem;
        margin-bottom: 1rem;
        font-size: 1.8rem !important;
    }
    h3 {
        font-size: 1.2rem !important;
        margin-bottom: 0.5rem !important;
    }
    .stButton>button {
        width: 140px;
        border-radius: 4px;
        height: 2.5em;
        font-size: 0.9rem;
        background-color: #f8f9fb;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.4rem !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.8rem !important;
    }
    [data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 5px 15px;
        border-radius: 6px;
        border: 1px solid #eeeeee;
    }
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 0.8rem;
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

st.sidebar.header("Filters")
selected_dept = st.sidebar.multiselect("Depts:", options=sorted(df['Department'].unique()), default=df['Department'].unique())
selected_gender = st.sidebar.multiselect("Gender:", options=df['Gender'].unique(), default=df['Gender'].unique())
selected_insurance = st.sidebar.multiselect("Insurance:", options=df['Insurance'].unique(), default=df['Insurance'].unique())
age_range = st.sidebar.slider("Age:", 0, 100, (0, 100))

mask = (df['Department'].isin(selected_dept)) & \
       (df['Gender'].isin(selected_gender)) & \
       (df['Insurance'].isin(selected_insurance)) & \
       (df['Age'].between(age_range[0], age_range[1]))
f_df = df[mask].copy()

st.markdown("<h1 style='text-align: center;'>HMO Resource Optimization Engine</h1>", unsafe_allow_html=True)

high_risk_total = f_df[f_df['Previous_NoShows'] >= 2]
total_risks = len(high_risk_total)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Apps", len(f_df))
m2.metric("High-Risk", total_risks)
m3.metric("Actioned", st.session_state.processed_count)
eff_gain = (st.session_state.processed_count / len(f_df) * 100) if len(f_df) > 0 else 0
m4.metric("Efficiency", f"+{eff_gain:.1f}%")

st.write("---")

st.markdown("<h3 style='text-align: center;'>Risk Management Console</h3>", unsafe_allow_html=True)

# מבנה ממוקד יותר
col_btn, col_tbl = st.columns([1, 4])

with col_btn:
    st.write("Next Batch:")
    if st.button("Flag 25"):
        if st.session_state.processed_count < total_risks:
            st.session_state.processed_count += min(25, total_risks - st.session_state.processed_count)
            st.rerun()
    
    if st.session_state.processed_count > 0:
        st.info(f"Active: {st.session_state.processed_count}")
    else:
        st.warning("Pending")

with col_tbl:
    risk_display = high_risk_total.head(6).astype(str)
    st.dataframe(risk_display[['AppointmentID', 'Department', 'Previous_NoShows', 'WaitTimeDays']], use_container_width=True, hide_index=True)

st.write("---")

st.markdown("<h3 style='text-align: center;'>Operational Heatmap</h3>", unsafe_allow_html=True)
f_df['Age_Bin'] = pd.cut(f_df['Age'], bins=[0, 20, 40, 60, 80, 100], labels=['0-20', '21-40', '41-60', '61-80', '81+'])
heat_data = f_df[f_df['Status'] == 'No-Show'].groupby(['Department', 'Age_Bin'], observed=False).size().reset_index(name='NoShows')
fig_heat = px.density_heatmap(heat_data, x='Age_Bin', y='Department', z='NoShows', color_continuous_scale='Reds', template='plotly_white')
fig_heat.update_layout(height=280, margin=dict(l=0, r=0, t=0, b=0))
st.plotly_chart(fig_heat, use_container_width=True)

st.write("---")
st.dataframe(f_df.reset_index(drop=True).astype(str).head(10), use_container_width=True, hide_index=True)
