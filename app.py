import streamlit as st
import pandas as pd
import glob
import os

st.set_page_config(page_title="Healthcare Analytics", layout="wide")
st.title("🏥 Healthcare Patient Analytics Portal")

# Auto-detect any CSV file in the folder
csv_files = glob.glob("*.csv")

if csv_files:
    # Load the first CSV file found
    file_path = csv_files[0]
    df = pd.read_csv(file_path)
    
    st.success(f"Data loaded successfully from: {file_path}")
    
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
    st.error("No CSV file found in this folder!")
    st.info("Current folder content: " + str(os.listdir(".")))
