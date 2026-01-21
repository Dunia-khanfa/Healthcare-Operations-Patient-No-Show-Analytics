import pandas as pd
import numpy as np
import sqlite3

# 1. Generate the data
num_records = 10000
np.random.seed(42)

data = {
    'AppointmentID': range(1000, 1000 + num_records),
    'PatientID': np.random.randint(1, 500, num_records),
    'DoctorID': np.random.randint(1, 50, num_records),
    'AppointmentDate': pd.to_datetime('2026-01-21'),
    'WaitTimeMinutes': np.random.randint(0, 60, num_records),
    'Status': np.random.choice(['Show', 'No-Show'], num_records)
}

df = pd.DataFrame(data)

# 2. Connect to SQL and create the table
conn = sqlite3.connect('healthcare_db.sql')
cursor = conn.cursor()

# Create the Appointments table structure
cursor.execute('''
CREATE TABLE IF NOT EXISTS Appointments (
    AppointmentID INT PRIMARY KEY,
    PatientID INT,
    DoctorID INT,
    AppointmentDate DATE,
    WaitTimeMinutes INT,
    Status VARCHAR(20)
)''')

# 3. Save the 10,000 rows into the SQL table
df.to_sql('Appointments', conn, if_exists='replace', index=False)

conn.close()
print(f"Successfully created SQL table 'Appointments' with {num_records} rows.")
