"""
Module to create a new user/admin roles.
Employees with User role will have login access to view employees data only,
while employees with Admin access will be able to add, update, delete employees data
and also assign user and admin roles to other employees.
"""
import asyncio
import os
import re
import sys
import streamlit as st

sys.path.append(os.path.abspath("."))

from src.backend import backend_modules
from src.log_handler import logger


st.header("Create a new User or Admin")

with st.form("new_user_admin_form"):
    assigned_role = st.selectbox("Role", ["User", "Admin"])
    firstname = st.text_input("First Name")
    lastname = st.text_input("Last Name")
    dob = st.date_input("Date of Birth")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    submit_button = st.form_submit_button("Save")


async def verify_user_details(email: str) -> bool | None:
    """
    Runs email and employee id verification concurrently.

    :param email: Email address to be verified.
    :return: Returns a boolean True if it exists, False if not, and None in case of error.
    """
    try:
        employee_id_task = backend_modules.verify_employee_id(email)
        email_task = backend_modules.verify_email(email, who="user")
        employee_id_exists, email_exists = await asyncio.gather(employee_id_task, email_task)
        return employee_id_exists, email_exists
    except Exception as e:
        st.error("Verification failed ❌.")
        st.error(f"Error details: {e}")
        return None, None


async def create_user() -> None:
    """Handles form submission with async API calls."""
    fields = {
        "Role": assigned_role,
        "First Name": firstname,
        "Last Name": lastname,
        "Date of Birth": dob,
        "Email": email,
        "Password": password,
        "Confirm Password": confirm_password,
    }

    missing_fields = [field for field, value in fields.items() if not value]
    email_valid_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if missing_fields:
        logger.error(f"Missing fields: {' ,'.join(missing_fields)}")
        st.error(f"Fields can't be empty: {' ❌, '.join(missing_fields)}")
        return

    if password != confirm_password:
        logger.error("Passwords do not match.")
        st.error("Passwords do not match ❌.")
        return

    if not re.match(email_valid_pattern, email):
        logger.error("Invalid email entered.")
        st.error("Invalid email! ❌ Please enter a correct email format.")
        return

    employee_id_exists, email_exists = await verify_user_details(email)

    if employee_id_exists is None or email_exists is None:
        if employee_id_exists is None:
            st.error("Employee ID verification failed ❌.")
            logger.error("Employee ID verification failed.")
        if email_exists is None:
            st.error("Email verification failed ❌.")
            logger.error("Email verification failed.")
        return

    if not employee_id_exists and isinstance(employee_id_exists, bool):
        logger.error(f"User with email {email} is not an employee.")
        st.error(f"User with email {email} is not an employee ❌.")
        return

    if email_exists:
        logger.error(f"User with email {email} is already in users table.")
        st.error(f"Email {email} is already used ❌. Already a user.")
        return

    else:
        try:
            response = await backend_modules.add_new_user(
                firstname=firstname,
                lastname=lastname,
                dob=dob,
                email=email,
                password=password,
                role=assigned_role,
                employee_id=employee_id_exists,
            )
            if response.get("status") == "Success":
                st.success(f"{response.get('message')} with assigned role {assigned_role} ✅.")
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
    loop.run_until_complete(create_user())
