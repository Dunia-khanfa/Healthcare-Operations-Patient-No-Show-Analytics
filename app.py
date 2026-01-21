import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Healthcare Analytics", layout="wide")
st.title("🏥 Healthcare Patient Analytics Portal")

# This is the 322 KB file we saw in your screenshot
file_path = 'healthcare_appointments_large.csv'

if os.path.exists(file_path):
    # READ_CSV - This is the fix! It doesn't look for tables.
    df = pd.read_csv(file_path)
    
    st.success("Loaded 10,000 records from CSV!")
    
    # Simple Metrics
    col1, col2 = st.columns(2)
    col1.metric("Total Appointments", len(df))
    col2.metric("No-Show Rate", f"{(df['Status'] == 'No-Show').mean()*100:.1f}%")
    
    # Chart
    st.subheader("Department Distribution")
    st.bar_chart(df['Department'].value_counts())
    
    st.dataframe(df.head(100))
else:
    st.error(f"Cannot find {file_path}. Are you in the right folder?")
