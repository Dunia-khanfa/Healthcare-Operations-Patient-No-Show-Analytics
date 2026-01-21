import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Healthcare Analytics", layout="wide")
st.title("🏥 Healthcare Patient Analytics Portal")

# Using the actual data file from your folder
file_name = 'healthcare_appointments_large.csv'

if os.path.exists(file_name):
    # Load the data directly from CSV
    df = pd.read_csv(file_name)
    
    st.success("Data loaded successfully from CSV!")
    
    # Display Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Appointments", len(df))
    
    if 'Status' in df.columns:
        no_show_rate = (df['Status'] == 'No-Show').mean() * 100
        col2.metric("No-Show Rate", f"{no_show_rate:.1f}%")
    
    # Show Charts
    if 'Department' in df.columns:
        st.subheader("Appointments by Department")
        st.bar_chart(df['Department'].value_counts())
    
    st.subheader("Data Preview")
    st.dataframe(df.head(100))
else:
    st.error(f"File '{file_name}' not found in the directory.")
