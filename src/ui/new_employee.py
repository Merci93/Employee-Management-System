"""
Module to add new employee data to the employees table.
"""

import asyncio
import os
import re
import sys

import streamlit as st

sys.path.append(os.path.abspath("."))

from src.backend import backend_modules
from src.log_handler import logger


st.header("Add New Employee")

with st.form("add_employee_form"):
    first_name = st.text_input("First Name")
    middle_name = st.text_input("Middle Name")
    last_name = st.text_input("Last Name")
    address = st.text_input("Address")
    dob = st.date_input("Date of Birth")
    gender = st.selectbox("Gender", ["Male", "Female"])
    phone = st.text_input("Phone Number")
    employee_positions = [
        "HR",
        "Data Engineer",
        "Solutions Architect",
        "Data Analyst",
        "Intern",
        "Business Analyst",
        "Senior Manager Engineering",
        "Data Scientist",
        "Junior Data Engineer",
        "Web Developer",
        "Cloud Architect",
        "Software Engineer",
        "Network Engineer",
        "DevOps Engineer",
        "Product Owner",
    ]
    position = st.selectbox("Position", employee_positions)
    email = st.text_input("Email")
    department = st.selectbox(
        "Department", ["IT", "Marketing", "Sales", "Research", "HR", "Data & Analytics"]
    )
    salary = st.number_input("Salary")
    hired_date = st.date_input("Hired Date")
    submit_button = st.form_submit_button("Save")


async def verify_email_and_phone(email: str, phone: str) -> bool | None:
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
        return phone_exists, email_exists  # type: ignore
    except Exception as e:
        st.error("Verification failed ❌.")
        st.error(f"Error details: {e}")
        return None, None  # type: ignore


async def get_ids(department: str, gender: str, position: str) -> int:
    """
    Gets the id for the department, gender and position of the new employee using the input data.

    :param department: Employee department.
    :param gender: Employee gender.
    :param position: Employee position.
    :return: Integer values for each of the items form their respective tables.
    """
    try:
        department_id_task = backend_modules.get_department_id(department)
        gender_id_task = backend_modules.get_gender_id(gender)
        position_id_task = backend_modules.get_position_id(position)
        dept_id, gender_id, position_id = await asyncio.gather(
            department_id_task, gender_id_task, position_id_task
        )
        return dept_id, gender_id, position_id  # type: ignore

    except Exception as e:
        st.error("ID retrieval failed ❌.")
        st.error(f"Error details: {e}")
        return None, None, None  # type: ignore


async def add_new_employee() -> None:
    """Handles form submission with async API calls to add new employee data"""
    fields = {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "address": address,
        "date_of_birth": dob,
        "gender_id": gender,
        "phone": phone,
        "position_id": position,
        "email": email,
        "department_id": department,
        "salary": salary,
        "hired_date": hired_date,
    }

    missing_fields = [field for field, value in fields.items() if not value]
    email_valid_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if missing_fields:
        logger.error(f"Missing fields: {' ,'.join(missing_fields)}")
        st.error(f"Fields can't be empty: {' ❌, '.join(missing_fields)}")
        return

    if not re.match(email_valid_pattern, email):
        logger.error("Invalid email entered.")
        st.error("Invalid email! ❌ Please enter a correct email format.")
        return

    phone_exists, email_exists = await verify_email_and_phone(phone=phone, email=email)  # type: ignore

    if phone_exists is None or email_exists is None:
        if phone_exists is None:
            st.error("Phone number verification failed ❌.")
            logger.error("Phone number verification failed.")
        if email_exists is None:
            st.error("Email verification failed ❌.")
            logger.error("Email verification failed.")
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
    dept_id, gender_id, position_id = await get_ids(department, gender, position)  # type: ignore

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
        fields["department_id"] = dept_id
        fields["gender_id"] = gender_id
        fields["position_id"] = position_id

        try:
            response = await backend_modules.add_new_employee_data(
                first_name=fields.get("first_name"),  # type: ignore
                middle_name=fields.get("middle_name"),  # type: ignore
                last_name=fields.get("last_name"),  # type: ignore
                address=fields.get("address"),  # type: ignore
                date_of_birth=fields.get("date_of_birth"),  # type: ignore
                gender_id=fields.get("gender_id"),  # type: ignore
                phone=fields.get("phone"),  # type: ignore
                position_id=fields.get("position_id"),  # type: ignore
                email=fields.get("email"),  # type: ignore
                department_id=fields.get("department_id"),  # type: ignore
                salary=fields.get("salary"),  # type: ignore
                hired_date=fields.get("hired_date"),  # type: ignore
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
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(add_new_employee())
