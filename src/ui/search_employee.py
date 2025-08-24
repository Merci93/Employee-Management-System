"""Module to search for employees data"""
import asyncio

import streamlit as st
import pandas as pd

from src.backend import backend_modules
from src.log_handler import logger


# Initialize session state if not already present
if 'employees_data' not in st.session_state:
    cols = [
        "Id", "First Name", "Middle Name", "Last Name", "Email", "Phone", "Address", "Salary",
        "Department", "Position", "Gender", "Date of Birth", "Hired Date", "Status", "Date Resigned"
    ]
    st.session_state.employees_data = pd.DataFrame(columns=cols)

st.header("Search Employee")

with st.form("search_employees_form"):
    search_option = st.selectbox("Search by", ["First Name", "Last Name", "Employee ID", "Department", "Role"])
    search_query = st.text_input("Enter search query")


async def get_employees_data() -> pd.DataFrame:
    """
    Get all data matching input parameter from the database.
    """
    pass


if st.button("Search"):
    pass  # Placeholder for search functionality
st.dataframe(st.session_state.employees_data)
