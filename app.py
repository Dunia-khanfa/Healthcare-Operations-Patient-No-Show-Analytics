import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="Healthcare Analytics", layout="wide")
st.title("🏥 Healthcare Patient Analytics Portal")

# File name we want to use
file_name = 'healthcare_appointments_large.csv'

# Check if file exists, if not, generate it right here!
if not os.path.exists(file_name):
    st.info("Creating data file in the current folder...")
    num_records = 10000
    np.random.seed(42)
    data = {
        'AppointmentID': range(1000, 1000 + num_records),
        'Age': np.random.randint(0, 95, num_records),
        'Department': np.random.choice(['Cardiology', 'Pediatrics', 'OPD', 'Orthopedics', 'General'], num_records),
        'WaitTimeDays': np.random.randint(0, 30, num_records),
        'Status': np.random.choice(['Show', 'No-Show'], num_records, p=[0.7, 0.3])
    }
    df_new = pd.DataFrame(data)
    df_new.to_csv(file_name, index=False)
    st.success(f"File '{file_name}' created successfully!")

# Now load the file (it definitely exists now)
df = pd.read_csv(file_path if 'file_path' in locals() else file_name)

# Dashboard Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Appointments", len(df))
col2.metric("No-Show Rate", f"{(df['Status'] == 'No-Show').mean()*100:.1f}%")
col3.metric("Avg Wait Time", f"{df['WaitTimeDays'].mean():.1f} Days")

# Charts
st.subheader("Department Distribution")
st.bar_chart(df['Department'].value_counts())

st.subheader("Data Preview")
st.dataframe(df.head(100))
