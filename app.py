import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(page_title="Patient Reliability System", layout="wide")

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

# --- Sidebar Filters ---
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

# --- KPIs (המספרים והאחוזים פה משתנים אוטומטית לפי המסננים) ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Appointments", len(f_df))

high_risk_patients = f_df[f_df['Previous_NoShows'] >= 2]
m2.metric("High-Risk Profiles", len(high_risk_patients))

# חישוב דינמי של אחוז ההתייעלות
efficiency = (len(high_risk_patients) / len(f_df) * 100) if len(f_df) > 0 else 0
m3.metric("Ready for Transfer", len(high_risk_patients))
m4.metric("Potential Efficiency", f"+{efficiency:.1f}%")

st.write("---")

# --- Risk Analysis Section ---
st.markdown("<h3 style='text-align: center;'>Risk Flagging for HMO Action</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>The system identifies slots for transfer. Final reallocation to be performed by HMO providers.</p>", unsafe_allow_html=True)

c_act, c_tbl = st.columns([1, 2])

with c_act:
    st.write("Click to flag high-risk records for the medical center's review.")
    if st.button("Flag for Reallocation"):
        st.success(f"Successfully flagged {len(high_risk_patients)} slots for HMO action.")
        st.balloons()

with c_tbl:
    # יצירת טבלה עם יישור ברירת מחדל (שמאל) שעובד תמיד
    risk_list = high_risk_patients.head(10).copy()
    risk_list['Action_Required'] = "HMO Transfer Ready"
    
    # הצגת הטבלה הממורכזת ויזואלית אך עם יישור פנימי לשמאל
    st.dataframe(
        risk_list[['AppointmentID', 'Department', 'Previous_NoShows', 'Action_Required']], 
        use_container_width=True, 
        hide_index=True
    )

st.write("---")

# --- Database ---
st.markdown("<h3 style='text-align: center;'>Full Patient Reliability Database</h3>", unsafe_allow_html=True)
# יישור סטנדרטי לשמאל שמונע שגיאות אדומות
st.dataframe(f_df.reset_index(drop=True), use_container_width=True, hide_index=True)
