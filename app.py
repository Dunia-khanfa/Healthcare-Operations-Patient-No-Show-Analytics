import streamlit as st
import pandas as pd
import numpy as np
import os
import sqlite3

st.set_page_config(page_title="Healthcare Patient Analytics", layout="wide")
st.title("🏥 Healthcare Patient Analytics - LIVE")

# 1. Create database automatically if missing
db_path = "healthcare_db.sql"

def create_database_if_missing():
    if not os.path.exists(db_path):
        st.warning("Database not found. Creating a new one...")
        num_records = 10000
        np.random.seed(42)
        data = {
            'AppointmentID': range(1, num_records + 1),
            'PatientID': np.random.randint(1, 500, num_records),
            'DoctorID': np.random.randint(1, 50, num_records),
            'AppointmentDate': pd.Timestamp.now().date(),
            'WaitTimeMinutes': np.random.randint(0, 60, num_records),
            'Status': np.random.choice(['Show', 'No-Show'], num_records, p=[0.7, 0.3])
        }
        df_temp = pd.DataFrame(data)
        conn = sqlite3.connect(db_path)
        df_temp.to_sql("Appointments", conn, if_exists="replace", index=False)
        conn.close()
        st.success("✅ Created new SQL database with 10,000 records!")

create_database_if_missing()

# 2. Load data from database
conn = sqlite3.connect(db_path)
df = pd.read_sql("SELECT * FROM Appointments", conn)
conn.close()

# 3. Display metrics and charts
st.success("The app is running successfully with SQL data!")

m1, m2, m3 = st.columns(3)
m1.metric("Total Appointments", len(df))
m2.metric("No-Show Rate", f"{(df['Status'] == 'No-Show').mean() * 100:.1f}%")
m3.metric("Avg Wait Time", f"{df['WaitTimeMinutes'].mean():.1f} Minutes")

st.subheader("Appointments by Doctor")
st.bar_chart(df['DoctorID'].value_counts().head(20))

st.subheader("Sample Appointment Data")
st.dataframe(df.head(100))
