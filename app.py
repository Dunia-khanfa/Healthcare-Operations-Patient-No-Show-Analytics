import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Healthcare Portal", layout="wide")
st.title("🏥 Healthcare Analytics Portal")

# This function creates the file and table if they are missing
def startup_db():
    conn = sqlite3.connect('healthcare_db.sql')
    cursor = conn.cursor()
    
    # Using the SQL structure you provided
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Patients (
        PatientID INT PRIMARY KEY,
        FullName VARCHAR(100),
        Age INT,
        City VARCHAR(50),
        ChronicCondition BOOLEAN 
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Doctors (
        DoctorID INT PRIMARY KEY,
        DoctorName VARCHAR(100),
        Department VARCHAR(50) 
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Appointments (
        AppointmentID INT PRIMARY KEY,
        PatientID INT,
        DoctorID INT,
        AppointmentDate DATE,
        WaitTimeMinutes INT,
        Status VARCHAR(20),
        FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
        FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID)
    )''')
    
    # Adding one row so the table isn't empty
    cursor.execute("INSERT OR IGNORE INTO Patients VALUES (1, 'System Test', 30, 'Local', 0)")
    cursor.execute("INSERT OR IGNORE INTO Doctors VALUES (1, 'System Doctor', 'General')")
    cursor.execute("INSERT OR IGNORE INTO Appointments VALUES (1, 1, 1, '2026-01-21', 0, 'Show')")
    
    conn.commit()
    conn.close()

def load_data():
    startup_db() # Run creation before loading
    conn = sqlite3.connect('healthcare_db.sql')
    try:
        df = pd.read_sql("SELECT * FROM Appointments", conn)
        return df
    except Exception as e:
        st.error(f"Database Error: {e}")
        return None
    finally:
        conn.close()

df = load_data()

if df is not None:
    st.success("Database is active")
    st.write("Current Appointments in System:")
    st.dataframe(df)
