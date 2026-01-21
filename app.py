import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Healthcare Analytics", layout="wide")
st.title("🏥 Healthcare Patient Analytics Portal")

def load_data():
    conn = sqlite3.connect('healthcare_db.sql')
    query = "SELECT * FROM Appointments"
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error: Table not found. Please run generate_health_data.py first. {e}")
        return None
    finally:
        conn.close()

df = load_data()

if df is not None:
    st.success("Data loaded successfully")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Appointments", len(df))
    
    if 'Status' in df.columns:
        no_show_rate = (df['Status'] == 'No-Show').mean() * 100
        col2.metric("No-Show Rate", f"{no_show_rate:.1f}%")
        
    if 'WaitTimeMinutes' in df.columns:
        col3.metric("Avg Wait Time", f"{df['WaitTimeMinutes'].mean():.1f} min")

    st.subheader("Raw Data Preview")
    st.dataframe(df.head(100))
    
    if 'Status' in df.columns:
        st.subheader("Appointment Status Distribution")
        st.bar_chart(df['Status'].value_counts())
