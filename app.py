import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Healthcare Analytics", layout="wide")
st.title("🏥 Healthcare Patient Analytics Portal")

# We use the CSV file that actually has data
file_path = 'healthcare_appointments_large.csv'

if os.path.exists(file_path):
    # This reads the CSV file directly, skipping any SQL database
    df = pd.read_csv(file_path)
    
    st.success("Success! Data loaded from CSV.")
    
    # Dashboard Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Appointments", len(df))
    
    if 'Status' in df.columns:
        no_show_rate = (df['Status'] == 'No-Show').mean() * 100
        col2.metric("No-Show Rate", f"{no_show_rate:.1f}%")
        
    if 'WaitTimeDays' in df.columns:
        col3.metric("Avg Wait Time (Days)", f"{df['WaitTimeDays'].mean():.1f}")

    # Visualizations
    st.subheader("Department Analysis")
    if 'Department' in df.columns:
        st.bar_chart(df['Department'].value_counts())

    st.subheader("Data Preview")
    st.dataframe(df.head(100))
else:
    st.error(f"Error: Could not find {file_path} in this folder.")
