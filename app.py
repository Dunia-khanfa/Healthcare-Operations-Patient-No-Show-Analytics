import streamlit as st
import pandas as pd
import numpy as np

# Force page config
st.set_page_config(page_title="Final Solution", layout="wide")

st.title("🏥 Healthcare Patient Analytics - LIVE")

# 1. GENERATE DATA INTERNALLY (No SQL, No CSV needed)
@st.cache_data
def load_final_data():
    num_records = 5000
    np.random.seed(42)
    data = {
        'AppointmentID': range(1, num_records + 1),
        'Age': np.random.randint(0, 95, num_records),
        'Department': np.random.choice(['Cardiology', 'Pediatrics', 'OPD', 'Orthopedics', 'General'], num_records),
        'WaitTimeDays': np.random.randint(0, 30, num_records),
        'Status': np.random.choice(['Show', 'No-Show'], num_records, p=[0.7, 0.3])
    }
    return pd.DataFrame(data)

df = load_final_data()

# 2. DISPLAY DASHBOARD
st.success("The app is now running independently of any database files!")

# Summary Metrics
m1, m2, m3 = st.columns(3)
m1.metric("Total Appointments", len(df))
m2.metric("No-Show Rate", f"{(df['Status'] == 'No-Show').mean()*100:.1f}%")
m3.metric("Avg Wait Time", f"{df['WaitTimeDays'].mean():.1f} Days")

# Visuals
st.subheader("Appointments by Department")
st.bar_chart(df['Department'].value_counts())

st.subheader("Patient Data Table")
st.dataframe(df.head(100))
