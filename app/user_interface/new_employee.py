"""
Module to add new employee data to the employees table.
"""

import asyncio
import re

import streamlit as st

from typing import Tuple

from backend import backend_modules
from config.config import settings
from logger.log_handler import logger


# Markdown to center headings
st.markdown("""
    <style>
    h1, h2, h3 {
        text-align: center;
    }
    div.stButton > button {
        display: block;
        margin: auto;
    }
    </style>
""", unsafe_allow_html=True)

st.header("Add New Employee")

with st.form("add_employee_form"):
    first_name = st.text_input("First Name")
    middle_name = st.text_input("Middle Name")
    last_name = st.text_input("Last Name")
    address = st.text_input("Address")
    dob = st.date_input("Date of Birth")
    gender = st.selectbox("Gender", settings.GENDER)
    phone = st.text_input("Phone Number")
    position = st.selectbox("Position", settings.POSITIONS)
    email = st.text_input("Email")
    department = st.selectbox("Department", settings.DEPARTMENTS)
    salary = st.number_input("Salary")
    hired_date = st.date_input("Hired Date")
    assigned_role = st.selectbox("Role", settings.ROLES)
    submit_button = st.form_submit_button("Save")
    # Add assigned role and assigne where else necessary


FIELDS = {
    "email": email,
    "phone": phone,
    "salary": salary,
    "address": address,
    "gender_id": gender,
    "date_of_birth": dob,
    "last_name": last_name,
    "position_id": position,
    "first_name": first_name,
    "hired_date": hired_date,
    "middle_name": middle_name,
    "department_id": department,
}


async def verify_email_and_phone(email: str, phone: str) -> Tuple[bool | None, bool | None]:
    """
    Runs email and phone number verification on employees database to ensure they don't already exist.

    :param email: New employee email address to be verified.
    :param phone: New employee phone number to be verified.
    :return: Boolean True if it already exists, False if not, and None in case of error.
    """
    try:
        phone_task = backend_modules.verify_phone_number(phone)
        email_task = backend_modules.verify_email(email, who="employee")
        phone_exists, email_exists = await asyncio.gather(phone_task, email_task)
        return phone_exists, email_exists
    except Exception as e:
        st.error("Verification failed ❌.")
        st.error(f"Error details: {e}")
        return None, None


async def get_ids(department: str, gender: str, position: str) -> Tuple[int | None, int | None, int | None]:
    """
    Gets the id for the department, gender and position of the new employee using the input data.

    :param department: Employee department.
    :param gender: Employee gender.
    :param position: Employee position.
    :return: Integer values for each of the items form their respective tables.
    """
    try:
        gender_id_task = backend_modules.get_gender_id(gender)
        position_id_task = backend_modules.get_position_id(position)
        department_id_task = backend_modules.get_department_id(department)
        dept_id, gender_id, position_id = await asyncio.gather(
            department_id_task, gender_id_task, position_id_task
        )
        return dept_id, gender_id, position_id

    except Exception as e:
        st.error("ID retrieval failed ❌.")
        st.error(f"Error details: {e}")
        return None, None, None


async def add_new_employee() -> None:
    """Handles form submission with async API calls to add new employee data"""

    missing_fields = [field for field, value in FIELDS.items() if not value]
    email_valid_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if missing_fields:
        logger.error(f"Missing fields: {' ,'.join(missing_fields)}")
        st.error(f"Fields can't be empty: {' ❌, '.join(missing_fields)}")
        return

    if not re.match(email_valid_pattern, email):
        logger.error("Invalid email entered.")
        st.error("Invalid email! ❌ Please enter a correct email format.")
        return

    phone_exists, email_exists = await verify_email_and_phone(phone=phone, email=email)

    if phone_exists is None or email_exists is None:
        if phone_exists is None:
            st.error("Phone number verification failed due to unkown error ❌.")
            logger.warning("Phone number verification failed. User with phone number already exists.")
        if email_exists is None:
            st.error("Email verification failed due to unknown error ❌.")
            logger.warning("Email verification failed. User with email already exists.")
        return

    if phone_exists:
        st.error(f"Phone number {phone} already exists in the database ❌.")
        logger.error(f"Phone number {phone} already exists in the database.")
        return

    if email_exists:
        logger.error(f"Employee with email {email} is already in employees table.")
        st.error(f"Email {email} is already used ❌.")
        return

    # Get the department, gender and position id's
    dept_id, gender_id, position_id = await get_ids(department, gender, position)

    if any(not value for value in (dept_id, gender_id, position_id)):
        if not dept_id:
            st.error("Failed to retrieve department id ❌.")
            logger.error("Failed to retrieve department id.")

        if not gender_id:
            st.error("Failed to retrieve gender id ❌.")
            logger.error("Failed to retrieve gender id.")

        if not position_id:
            st.error("Failed to retrieve position id ❌.")
            logger.error("Failed to retrieve position id.")
        return

    else:
        FIELDS["department_id"] = dept_id
        FIELDS["gender_id"] = gender_id
        FIELDS["position_id"] = position_id

        try:
            response = await backend_modules.add_new_employee_data(
                email=FIELDS.get("email"),  # type: ignore
                phone=FIELDS.get("phone"),  # type: ignore
                salary=FIELDS.get("salary"),  # type: ignore
                address=FIELDS.get("address"),  # type: ignore
                gender_id=FIELDS.get("gender_id"),  # type: ignore
                last_name=FIELDS.get("last_name"),  # type: ignore
                hired_date=FIELDS.get("hired_date"),  # type: ignore
                first_name=FIELDS.get("first_name"),  # type: ignore
                middle_name=FIELDS.get("middle_name"),  # type: ignore
                position_id=FIELDS.get("position_id"),  # type: ignore
                date_of_birth=FIELDS.get("date_of_birth"),  # type: ignore
                department_id=FIELDS.get("department_id"),  # type: ignore
            )

            if response.get("status") == "Success":
                st.success(f"{response.get('message')} ✅.")
            else:
                st.error(f"{response.get('message')} ❌.")
                logger.error(f"{response.get('message')}.")
        except Exception as e:
            st.error("Failed to create user ❌. Please try again.")
            st.error(f"Error details: {e}")
            logger.error(f"Failed to create user. Error: {e}.")


if submit_button:
    asyncio.run(add_new_employee())
