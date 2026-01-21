import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="Healthcare Analytics", layout="wide")
st.title("🏥 Healthcare Patient Analytics Portal")

# שם הקובץ שהאפליקציה תיצור ותשתמש בו
file_name = 'healthcare_data.csv'

# אם הקובץ לא קיים בתיקייה הזו, ניצור אותו עכשיו אוטומטית
if not os.path.exists(file_name):
    st.info("מייצר נתונים חדשים בתיקייה... אנא המתיני.")
    num_records = 5000
    np.random.seed(42)
    df_gen = pd.DataFrame({
        'AppointmentID': range(1000, 1000 + num_records),
        'Age': np.random.randint(0, 95, num_records),
        'Department': np.random.choice(['Cardiology', 'Pediatrics', 'OPD', 'Orthopedics', 'General'], num_records),
        'Status': np.random.choice(['Show', 'No-Show'], num_records, p=[0.7, 0.3])
    })
    df_gen.to_csv(file_name, index=False)
    st.success("הנתונים נוצרו בהצלחה!")

# טעינת הנתונים
df = pd.read_csv(file_name)

# הצגת המדדים והגרפים
col1, col2 = st.columns(2)
col1.metric("סה\"כ תורים", len(df))
col2.metric("אחוז אי-הופעה", f"{(df['Status'] == 'No-Show').mean()*100:.1f}%")

st.subheader("התפלגות לפי מחלקות")
st.bar_chart(df['Department'].value_counts())

st.subheader("תצוגת נתונים")
st.dataframe(df.head(50))
