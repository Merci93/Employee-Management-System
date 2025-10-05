"""Module to update employee data."""
import asyncio
import streamlit as st
import pandas as pd

from src.backend import backend_modules
from src.config import settings


DATA_TO_UPDATE = settings.DATA_TO_UPDATE
POSITIONS = settings.POSITIONS
DEPARTMENTS = settings.DEPARTMENTS


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
    data_to_update: str,
    updated_value: str | int | float
) -> bool:
    """
    A function to update employee information with given data.

    :return: Boolean True if update was successful, False, otherwise
    """
    DATA_MAPPING = {
        "Address": "address",
        "Salary": "salary",
        "First Name": "first_name",
        "Middle Name": "middle_name",
        "Last Name": "last_name",
        "Position": "position",
        "Department": "department",
        "Phone": "phone"
    }

    # Build keyword arguments with all fields defaulted to None
    kwargs = {v: None for v in DATA_MAPPING.values()}

    if data_to_update in DATA_MAPPING:
        field_name = DATA_MAPPING[data_to_update]
        kwargs[field_name] = updated_value  # type: ignore
    else:
        raise ValueError(f"Invalid field: {data_to_update}")

    update_status = await backend_modules.update_employee_data(
        employee_id=employee_id,
        **kwargs
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
elif data_to_update == "Position":
    updated_value = st.selectbox(f"Enter new {data_to_update}", POSITIONS)
elif data_to_update == "Department":
    updated_value = st.selectbox(f"Enter new {data_to_update}", DEPARTMENTS)
else:
    updated_value = st.text_input(f"Enter new {data_to_update}", key="updated_value")

with st.form("employee_data_update_form"):
    submit_button = st.form_submit_button("Update Data")

if submit_button:
    st.write(f"Updating employee {data_to_update} ...")
    if employee_id.strip().isdigit():
        success = asyncio.run(update_employee_data(
            employee_id=int(employee_id),
            data_to_update=data_to_update,
            updated_value=updated_value
        ))
        if success:
            st.success(f"{data_to_update} updated successfully for employee {employee_id}.")
        else:
            st.error("Update failed. Please try again.")
    else:
        st.error("Invalid Employee ID. Please enter a numeric value.")
