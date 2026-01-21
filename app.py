import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="Healthcare Analytics", layout="wide")
st.title("🏥 Healthcare Patient Analytics Portal")

# שם הקובץ שאנחנו מחפשים
file_name = 'healthcare_appointments_large.csv'

# בדיקה: אם הקובץ לא קיים בתיקייה הזו, ניצור אותו עכשיו עם נתונים אקראיים
if not os.path.exists(file_name):
    st.warning("Data file not found. Generating new dataset...")
    num_records = 5000
    np.random.seed(42)
    df_gen = pd.DataFrame({
        'AppointmentID': range(1000, 1000 + num_records),
        'Age': np.random.randint(0, 95, num_records),
        'Department': np.random.choice(['Cardiology', 'Pediatrics', 'OPD', 'Orthopedics', 'General'], num_records),
        'WaitTimeDays': np.random.randint(0, 30, num_records),
        'Status': np.random.choice(['Show', 'No-Show'], num_records, p=[0.7, 0.3])
    })
    df_gen.to_csv(file_name, index=False)
    st.success("Dataset created successfully!")

# טעינת הנתונים מהקובץ (CSV)
df = pd.read_csv(file_name)

# הצגת נתונים בלוח הבקרה
col1, col2, col3 = st.columns(3)
col1.metric("Total Appointments", len(df))
col2.metric("No-Show Rate", f"{(df['Status'] == 'No-Show').mean()*100:.1f}%")
col3.metric("Avg Wait Time", f"{df['WaitTimeDays'].mean():.1f} Days")

st.subheader("Department Distribution")
st.bar_chart(df['Department'].value_counts())

st.subheader("Recent Records")
st.dataframe(df.head(100))
