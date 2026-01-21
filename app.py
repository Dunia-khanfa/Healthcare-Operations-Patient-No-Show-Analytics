import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(page_title="Advanced Patient Analytics", layout="wide")

def get_data():
    file_name = 'healthcare_data_final.csv'
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        num_records = 5000
        np.random.seed(42)
        df = pd.DataFrame({
            'AppointmentID': range(1000, 1000 + num_records),
            'Age': np.random.randint(0, 95, num_records),
            'Department': np.random.choice(['Cardiology', 'Pediatrics', 'OPD', 'Orthopedics', 'General'], num_records),
            'WaitTimeDays': np.random.randint(0, 30, num_records),
            'Status': np.random.choice(['Show', 'No-Show'], num_records, p=[0.78, 0.22]),
            'Gender': np.random.choice(['Male', 'Female'], num_records),
            'Insurance': np.random.choice(['Private', 'Public', 'None'], num_records)
        })
        df.to_csv(file_name, index=False)
        return df

df = get_data()

st.sidebar.header("📊 Filter Dashboard")
selected_dept = st.sidebar.multiselect("Select Departments:", options=sorted(df['Department'].unique()), default=df['Department'].unique())
age_range = st.sidebar.slider("Age Range:", 0, 100, (0, 100))
selected_insurance = st.sidebar.radio("Insurance Type:", options=['All', 'Private', 'Public', 'None'], horizontal=True)

mask = (df['Department'].isin(selected_dept)) & (df['Age'].between(age_range[0], age_range[1]))
if selected_insurance != 'All':
    mask &= (df['Insurance'] == selected_insurance)
f_df = df[mask]

st.title("🏥 Healthcare Operations & Patient Analytics")
st.markdown(f"**Live Statistics for {len(f_df)} appointments**")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Appointments", len(f_df))
m2.metric("No-Show Rate", f"{(f_df['Status']=='No-Show').mean()*100:.1f}%")
m3.metric("Average Patient Age", int(f_df['Age'].mean()))
m4.metric("Avg Wait Time", f"{f_df['WaitTimeDays'].mean():.1f} Days")

st.write("---")

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Appointment Status by Department")
    fig_dept = px.histogram(f_df, x="Department", color="Status", 
                            barmode="group",
                            template="plotly_white",
                            color_discrete_map={'Show':'#2ecc71', 'No-Show':'#e74c3c'})
    fig_dept.update_layout(xaxis_tickangle=0, font=dict(size=14))
    st.plotly_chart(fig_dept, use_container_width=True)

with col_right:
    st.subheader("📈 Attendance Rate by Age Group")
    f_df['AgeGroup'] = pd.cut(f_df['Age'], bins=[0, 18, 40, 65, 100], labels=['Kids', 'Young Adults', 'Middle Aged', 'Seniors'])
    age_data = f_df.groupby(['AgeGroup', 'Status'], observed=False).size().reset_index(name='count')
    fig_age = px.bar(age_data, x="AgeGroup", y="count", color="Status", 
                     barmode="stack", template="plotly_white")
    fig_age.update_layout(xaxis_tickangle=0, font=dict(size=14))
    st.plotly_chart(fig_age, use_container_width=True)

st.write("---")

c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("⏳ Wait Time Distribution & Impact")
    fig_wait = px.area(f_df.groupby('WaitTimeDays').size().reset_index(name='Volume'), 
                       x='WaitTimeDays', y='Volume', title="Appointment Volume Over Wait Duration")
    st.plotly_chart(fig_wait, use_container_width=True)

with c2:
    st.subheader("💳 Insurance Split")
    fig_pie = px.pie(f_df, names='Insurance', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_pie, use_container_width=True)

with st.expander("📂 Access Raw Patient Database"):
    st.dataframe(f_df, use_container_width=True)
