import pandas as pd
import numpy as np
import sqlite3

# 1. Create data
num_records = 10000
np.random.seed(42)

data = {
    'AppointmentID': range(1000, 1000 + num_records),
    'PatientID': np.random.randint(1, 500, num_records),
    'DoctorID': np.random.randint(1, 50, num_records),
    'AppointmentDate': '2026-01-21',
    'WaitTimeMinutes': np.random.randint(0, 60, num_records),
    'Status': np.random.choice(['Show', 'No-Show'], num_records)
}

df = pd.DataFrame(data)

# 2. Build the SQL database
conn = sqlite3.connect('healthcare_db.sql')
# This line creates the 'Appointments' table and fills it with data
df.to_sql('Appointments', conn, if_exists='replace', index=False)

conn.close()
print("Successfully created Appointments table in SQL!")
