import pandas as pd
import numpy as np


num_records = 10000

np.random.seed(42)

data = {
    'AppointmentID': range(1000, 1000 + num_records),
    'Age': np.random.randint(0, 95, num_records),
    'Gender': np.random.choice(['M', 'F'], num_records),
    'Department': np.random.choice(['Cardiology', 'Pediatrics', 'OPD', 'Orthopedics', 'General'], num_records),
    'WaitTimeDays': np.random.randint(0, 45, num_records),
    'ChronicCondition': np.random.choice([0, 1], num_records, p=[0.7, 0.3]),
    'SMS_Received': np.random.choice([0, 1], num_records),
}

df = pd.DataFrame(data)


def predict_status(row):
    chance = 0.7 # בסיס של 70% הגעה
    if row['SMS_Received'] == 1: chance += 0.15
    if row['Age'] > 60: chance += 0.1
    if row['WaitTimeDays'] > 20: chance -= 0.2
    
    return 'Show' if np.random.random() < chance else 'No-Show'

df['Status'] = df.apply(predict_status, axis=1)


df.to_csv('healthcare_appointments_large.csv', index=False)
print(f"Successfully generated {num_records} records in healthcare_appointments_large.csv")
