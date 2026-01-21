import streamlit as st
import pandas as pd
import sqlite3
import numpy as np

st.set_page_config(page_title="Healthcare Analytics", layout="wide")
st.title("🏥 Healthcare Patient Analytics Portal")

# Function to create the database and table if they don't exist
def ensure_database_ready():
    conn = sqlite3.connect('healthcare_db.sql')
    cursor = conn.cursor()
    
    # 1. Create the table based on your SQL structure
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Appointments (
        AppointmentID INT PRIMARY KEY,
        Age INT,
        Department VARCHAR(50),
        WaitTimeMinutes INT,
        Status VARCHAR(20)
    )''')
    
    # 2. Check if the table is empty
    cursor.execute("SELECT count(*) FROM Appointments")
    if cursor.fetchone()[0] == 0:
        st.info("Generating 10,000 records for the first time... please wait.")
        # Generate dummy data
        num_records = 10000
        np.random.seed(42)
        data = {
            'AppointmentID': range(1000, 1000 + num_records),
            'Age': np.random.randint(0, 95, num_records),
            'Department': np.random.choice(['Cardiology', 'Pediatrics', 'OPD', 'Orthopedics', 'General'], num_records),
            'WaitTimeMinutes': np.random.randint(0, 60, num_records),
            'Status': np.random.choice(['Show', 'No-Show'], num_records, p=[0.7, 0.3])
        }
        df_temp = pd.DataFrame(data)
        # Save to SQL
        df_temp.to_sql('Appointments', conn, if_exists='replace', index=False)
        st.success("10,000 records created successfully!")
    
    conn.close()

# Execute database check
ensure_database_ready()

# Load Data
def load_data():
    conn = sqlite3.connect('healthcare_db.sql')
    try:
        df = pd.read_sql("SELECT * FROM Appointments", conn)
        return df
    except Exception as e:
        st.error(f"Error reading from database: {e}")
        return None
    finally:
        conn.close()

df = load_data()

if df is not None:
    # Key Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Appointments", len(df))
    
    no_show_rate = (df['Status'] == 'No-Show').mean() * 100
    col2.metric("No-Show Rate", f"{no_show_rate:.1f}%")
    
    avg_wait = df['WaitTimeMinutes'].mean()
    col3.metric("Avg Wait Time", f"{avg_wait:.1f} min")

    # Visuals
    st.subheader("Appointments by Department")
    st.bar_chart(df['Department'].value_counts())

    st.subheader("Raw Data Preview")
    st.dataframe(df.head(100))
