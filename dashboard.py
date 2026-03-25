import streamlit as st
import sqlite3
import pandas as pd

def show_analytics():
    st.header("📊 Hospital Analytics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Patients",
            "1,234",
            "+12% this month"
        )
    with col2:
        st.metric(
            "Appointments",
            "456",
            "+8% this month"
        )
    with col3:
        st.metric(
            "AI Consultations",
            "2,890",
            "+25% this month"
        )
    with col4:
        st.metric(
            "Revenue",
            "₹45,000",
            "+15% this month"
        )