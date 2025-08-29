"""Module to search for employees data"""
import asyncio

import streamlit as st
import pandas as pd

from src.backend import backend_modules


# Initialize session state if not already present
if 'employees_data' not in st.session_state:
    cols = [
        "id", "first_name", "middle_name", "last_name", "email", "phone", "address", "salary",
        "department", "position", "gender", "date_of_birth", "hired_date", "status", "date_resigned"
    ]
    st.session_state.employees_data = pd.DataFrame(columns=cols)

st.header("Search Employee")

with st.form("search_employees_form"):
    search_option = st.selectbox("Search by", ["First Name", "Last Name", "Employee ID", "Department", "Position"])
    search_query = st.text_input("Enter search query")
    submit_button = st.form_submit_button("Search")


async def get_employees_data(search_option: str, search_query: str) -> pd.DataFrame | None:
    """
    Get all data matching input parameter from the database.
    """
    #  Search option mapping with client functions
    options = {
        "Employee ID": ("id", backend_modules.get_employee_data_by_id),
        "Position": ("position", backend_modules.get_employee_data_by_position),
        "Last Name": ("last_name", backend_modules.get_employee_data_by_last_name),
        "First Name": ("first_name", backend_modules.get_employee_data_by_first_name),
        "Department": ("department", backend_modules.get_employee_data_by_department),
    }

    query = search_query.strip()
    if not query:
        st.error("Empty strings are not allowed. Please enter a valid search parameter.")
        return

    select_options = options.get(search_option)
    if not select_options:
        st.error(f"Invalid search option: {search_option}")
        return

    field, func = select_options

    #  Special case for employee ID's to validate entered data are all integers
    if field == "id":
        if not query.isdigit():
            st.error("Invalid Employee ID. Please enter a numeric value.")
            return
        return await func(int(query))

    #  Run other searches
    return await func(query)


if submit_button:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    st.session_state.employees_data = loop.run_until_complete(get_employees_data(search_option, search_query))
