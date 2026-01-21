import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
import os

st.set_page_config(page_title="Healthcare Analytics", layout="wide")
st.title("🏥 Healthcare Patient Analytics Portal")

# Use the exact filename from your folder
db_file = 'healthcare.sql'

def initialize_database():
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create the table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Appointments (
        AppointmentID INTEGER PRIMARY KEY,
        Age INTEGER,
        Department TEXT,
        WaitTimeMinutes INTEGER,
        Status TEXT
    )''')
    
    # Check if empty
    cursor.execute("SELECT count(*) FROM Appointments")
    if cursor.fetchone()[0] == 0:
        # Generate 1000 rows immediately
        num_records = 1000
        df_init = pd.DataFrame({
            'AppointmentID': range(1, num_records + 1),
            'Age': np.random.randint(0, 95, num_records),
            'Department': np.random.choice(['Cardiology', 'Pediatrics', 'General'], num_records),
            'WaitTimeMinutes': np.random.randint(0, 60, num_records),
            'Status': np.random.choice(['Show', 'No-Show'], num_records)
        })
        df_init.to_sql('Appointments', conn, if_exists='replace', index=False)
    
    conn.commit()
    conn.close()

# Run initialization
initialize_database()

# Load and Display
conn = sqlite3.connect(db_file)
df = pd.read_sql("SELECT * FROM Appointments", conn)
conn.close()

st.success("Connected to database successfully!")
st.metric("Total Records Found", len(df))
st.bar_chart(df['Department'].value_counts())
st.dataframe(df.head(50))
