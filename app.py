 import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Healthcare Analytics", layout="wide")
st.title("🏥 Healthcare Patient Analytics Portal")

# Check if the CSV file exists
file_path = 'healthcare_appointments_large.csv'

if os.path.exists(file_path):
    # Load the CSV data directly
    df = pd.read_sql = pd.read_csv(file_path)
    
    st.success("Data loaded successfully from CSV!")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Appointments", len(df))
    
    if 'Status' in df.columns:
        no_show_rate = (df['Status'] == 'No-Show').mean() * 100
        col2.metric("No-Show Rate", f"{no_show_rate:.1f}%")
    
    # Show data
    st.subheader("Recent Appointments")
    st.dataframe(df.head(100))
    
    # Simple Chart
    if 'Department' in df.columns:
        st.subheader("Appointments by Department")
        st.bar_chart(df['Department'].value_counts())
else:
    st.error(f"File not found: {file_path}")
    st.info("Please run 'python generate_health_data.py' first to create the data.")
