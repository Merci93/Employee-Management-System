"""Module to update employee data."""
import asyncio
import streamlit as st
import pandas as pd

from src.backend import backend_modules
from src.config import settings


DATA_TO_UPDATE = settings.DATA_TO_UPDATE


def update_input():
    """Function to update session state for input reset"""
    st.session_state.updated_value = ""


async def get_employee_data(employee_id: int) -> pd.DataFrame:
    """
    Get employee data using the employee ID.
    :param employee_id: ID of employee
    :return: Pandas Dataframe with employee data or an empty DataFrame.
    """
    df = await backend_modules.get_employee_data_by_id(employee_id=employee_id)
    return df if df is not None else pd.DataFrame()  # type: ignore


async def update_employee_data(
    employee_id: int,
    address: str | None = None,
    salary: int | float | None = None,
    first_name: str | None = None,
    middle_name: str | None = None,
    last_name: str | None = None,
    position: str | None = None,
    department: str | None = None,
    phone: int | None = None,
) -> bool:
    """
    A function to update employee information with given data.

    :return: Boolean True if update was successful, False, otherwise
    """
    update_status = await backend_modules.update_employee_data(
        employee_id=employee_id,
        address=address,
        salary=salary,
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        position=position,
        department=department,
        phone=phone
    )
    return update_status


st.header("Update Employee Data")

# Initialize session state variables
if "employee_data" not in st.session_state:
    st.session_state.employee_data = None
if "selected_update_field" not in st.session_state:
    st.session_state.selected_update_field = "Address"
if "updated_value" not in st.session_state:
    st.session_state.updated_value = ""


with st.form("employee_id_search_form"):
    employee_id = st.text_input("Enter Employee ID")
    get_available_employee_data = st.form_submit_button("Verify Existing Employee Data")


if get_available_employee_data:
    if employee_id.strip().isdigit():
        st.session_state.employee_data = asyncio.run(get_employee_data(int(employee_id)))
    else:
        st.error("Invalid Employee ID. Please enter a numeric value.")

if st.session_state.employee_data is not None and not st.session_state.employee_data.empty:
    st.write("### Employee Data:")
    st.dataframe(st.session_state.employee_data)
else:
    st.write(f"Employee with ID {employee_id} does not exist.")

data_to_update = st.selectbox(
    "### Data to Update",
    DATA_TO_UPDATE,
    key="selected_update_field",
    on_change=update_input,
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
