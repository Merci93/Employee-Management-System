"""Module to update employee data."""
import asyncio
import streamlit as st
import pandas as pd

from src.backend import backend_modules


st.header("Update Employee Data")

# Initialize session state variables
if "employee_data" not in st.session_state:
    st.session_state.employee_data = None
if "selected_update_field" not in st.session_state:
    st.session_state.selected_update_field = "Address"
if "updated_value" not in st.session_state:
    st.session_state.updated_value = ""


def update_input():
    """Function to update session state for input reset"""
    st.session_state.updated_value = ""


with st.form("employee_id_search_form"):
    employee_id = st.text_input("Enter Employee ID")
    get_available_employee_data = st.form_submit_button("Verify Existing Employee Data")


async def get_employee_data(employee_id: int) -> pd.DataFrame:
    """
    Get employee data using the employee ID.
    :param employee_id: ID of employee
    :return: Pandas Dataframe with employee data or an empty DataFrame.
    """
    df = await backend_modules.get_employee_data(employee_id=employee_id)
    return df if df is not False else pd.DataFrame()  # type: ignore


if get_available_employee_data:
    if employee_id.strip().isdigit():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        st.session_state.employee_data = loop.run_until_complete(get_employee_data(int(employee_id)))
    else:
        st.error("Invalid Employee ID. Please enter a numeric value.")

if st.session_state.employee_data is not None and not st.session_state.employee_data.empty:
    st.write("### Employee Data:")
    st.dataframe(st.session_state.employee_data)
else:
    st.write(f"Employee with ID {employee_id} does not exist.")

data_to_update = st.selectbox(
    "Data to Update",
    ["Address", "Phone", "Department", "Position", "Salary"],
    key="selected_update_field",
    on_change=update_input
)

# Dynamic input field for updates
if data_to_update == "Salary":
    updated_value = st.number_input(f"Enter new {data_to_update}", min_value=0, step=1)
else:
    updated_value = st.text_input(f"Enter new {data_to_update}", key="updated_value")

with st.form("employee_data_update_form"):
    submit_button = st.form_submit_button("Update Data")

if submit_button:
    st.write(f"Updating {data_to_update} to {updated_value} ...")
