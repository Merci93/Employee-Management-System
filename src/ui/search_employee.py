"""Module to search for employees data"""
import asyncio

import streamlit as st
import pandas as pd

from src.config import settings
from src.backend import backend_modules

# Markdown ro center headings
st.markdown("""
    <style>
    h1, h2, h3 {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

POSITIONS = settings.POSITIONS
DEPARTMENTS = settings.DEPARTMENTS
EMPLOYEE_COLUMNS = settings.EMPLOYEES_COLUMN

#  Search option mapping with client functions
OPTIONS = {
    "Employee ID": ("id", backend_modules.get_employee_data_by_id),
    "Position": ("position", backend_modules.get_employee_data_by_position),
    "Last Name": ("last_name", backend_modules.get_employee_data_by_last_name),
    "First Name": ("first_name", backend_modules.get_employee_data_by_first_name),
    "Department": ("department", backend_modules.get_employee_data_by_department),
}

# Input widgets definition
input_widgets = {
    "Department": lambda: st.selectbox("Select Department", DEPARTMENTS),
    "Position": lambda: st.selectbox("Select Position", POSITIONS),
    "First Name": lambda: st.text_input("Enter First Name"),
    "Last Name": lambda: st.text_input("Enter Last Name"),
    "Employee ID": lambda: st.text_input("Enter Employee ID"),
}


async def get_employees_data(search_option: str, search_query: str) -> pd.DataFrame:
    """
    Get all data matching input parameter from the database.
    """
    query = search_query.strip()
    if not query:
        st.error("Empty strings are not allowed. Please enter a valid search parameter.")
        return pd.DataFrame()

    field, func = OPTIONS.get(search_option, (None, None))
    if not field or not func:
        st.error(f"Invalid search option: {search_option}")
        return pd.DataFrame()

    #  Special case for employee ID's to validate entered data are all integers
    if field == "id":
        if not query.isdigit():
            st.error("Invalid Employee ID. Please enter a numeric value.")
            return pd.DataFrame()
        return await func(int(query))

    #  Run other searches
    return await func(query)


# Initialize session state if not already present
if 'employees_data' not in st.session_state:
    cols = [
        "id", "first_name", "middle_name", "last_name", "email", "phone", "address", "salary",
        "department", "position", "gender", "date_of_birth", "hired_date", "status", "date_resigned"
    ]
    st.session_state.employees_data = pd.DataFrame(columns=cols)

st.header("Search Employee")

# Select search option
search_option = st.selectbox(
    "Search by",
    ["First Name", "Last Name", "Employee ID", "Department", "Position"]
)

# Dynmaic input based selection
if search_option == "Department":
    search_query = st.selectbox("Select Department", DEPARTMENTS)
elif search_option == "Position":
    search_query = st.selectbox("Select Position", POSITIONS)
elif search_option == "Employee ID":
    search_query = st.text_input("Enter Employee ID")
elif search_option == "First Name":
    search_query = st.text_input("Enter First Name")
else:
    search_query = st.text_input("Enter Last Name")


if st.button("Search"):
    st.session_state.employees_data = asyncio.run(
        get_employees_data(search_option, search_query)
    )

if st.session_state.employees_data is not None and not st.session_state.employees_data.empty:
    st.write("### Employee Data:")
    st.dataframe(st.session_state.employees_data)
else:
    st.write("No data found for the search value.")
