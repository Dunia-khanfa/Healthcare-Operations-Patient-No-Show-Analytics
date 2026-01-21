import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.title("🏥 Healthcare Patient Analytics Portal")


conn = sqlite3.connect('healthcare.db')


query = "SELECT * FROM Appointments"
df = pd.read_sql(query, conn)

col1, col2 = st.columns(2)
total_apps = len(df)
no_show_rate = (df[df['Status'] == 'No-Show'].shape[0] / total_apps) * 100

col1.metric("Total Appointments", total_apps)
col2.metric("No-Show Rate", f"{no_show_rate:.1f}%")


dept = st.selectbox("Select Department", df['Department'].unique())
filtered_df = df[df['Department'] == dept]

fig = px.histogram(filtered_df, x="Age", color="Status", title=f"Age Distribution in {dept}")
st.plotly_chart(fig)


st.write("### Raw Data from SQL Server", filtered_df)
