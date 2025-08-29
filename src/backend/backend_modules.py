""""Backend module"""
from datetime import date
from typing import Dict

import httpx
import pandas as pd
from fastapi import HTTPException

from src.log_handler import logger


BASE_URL = "http://localhost:8000/v1"
HEADERS = {"accept": "application/json"}


# async def verify_employee_id(email: str) -> bool:
#     """
#     Verify if the user to be added is an employee.

#     :param Email: Employee email to check.
#     return: A boolean True if it exists, False otherwise.
#     """
#     logger.info("Starting Employee ID verification...")

#     url = f"{BASE_URL}/verify_employee_id/"
#     params = {
#         "email": email,
#     }
#     async with httpx.AsyncClient() as client:
#         response = await client.get(url, params=params, headers=HEADERS)
#         response.raise_for_status()
#         logger.info("Employee ID verification completed.")
#         response = response.json()

#         if response.get("exist"):
#             return response.get("value")

#         logger.error(f"User with email {email} is not an employee.")
#         return response.get("value", False)


async def verify_parameter(base_path: str, identifier: str | int, log_context: str, params: dict | None = None) -> bool:
    """
    Helper function to verify/validate identifier existence in the database and return true or false.

    :param base_path: API base path
    :param identifier: Employee identifier
    :param log_context: Context for logging messages
    :param params: Optional query parameters to include in the request
    :return: True if exists, False otherwise.
    """
    logger.info(f"Starting verification for {log_context}: {identifier} ...")

    url = f"{BASE_URL}/{base_path}/{identifier}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=HEADERS)
        response.raise_for_status()
        response = response.json()

        exists = response.get("exist", False)

        if exists:
            logger.info(f"{log_context.capitalize()} with email {identifier} already exists.")
        else:
            logger.info(f"{log_context.capitalize()} {identifier} does not exist.")

        return exists


async def verify_email(email: str, who: str) -> bool:
    """
    Verify if user email already exists in the database.

    :param Email: Input email to check.
    :param who: Input parameter to either verify employee email or user/admin email.
    return: A boolean True if it exists, False otherwise.
    """
    return await verify_parameter(
        base_path="verify_email",
        identifier=email,
        log_context="email",
        params={"who": who}
    )


async def verify_phone_number(phone_number: str) -> bool:
    """
    Verify if phone number already exists in database.

    :param phone: Phone number to verify.
    :return: Boolean True if esist, False otherwise.
    """
    return await verify_parameter(
        base_path="verify_phone_number",
        identifier=phone_number,
        log_context="phone number"
    )


async def fetch_parameter_id(base_path: str, identifier: str, log_context: str) -> int | bool:
    """
    Helper function to fetch parameter id from database and return a value.

    :param base_path: API base path
    :param identifier: Employee identifier
    :param log_context: Context for logging messages
    """
    logger.info(f"Starting {log_context} ID retrieval for {log_context}: {identifier}")
    url = f"{BASE_URL}/{base_path}/{identifier}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=HEADERS)
        response.raise_for_status()
        response = response.json()

        required_id = response.get("value", False)

        if required_id:
            logger.info(f"{log_context.capitalize()} ID retrieved successfully.")
            return required_id

        logger.info(f"{log_context.capitalize()} ID not retrieved.")
        return required_id


async def get_gender_id(gender: str) -> int | bool:
    """
    Get the gender ID for the employee.

    :param gender: Gender
    :return: Gender ID from the gender table.
    """
    return await fetch_parameter_id(
        base_path="get_gender_id",
        identifier=gender,
        log_context="gender"
    )


async def get_department_id(department: str) -> int | bool:
    """
    Get the department ID for the employee.

    :param department: Department
    :return: Department ID from the department table.
    """
    return await fetch_parameter_id(
        base_path="get_department_id",
        identifier=department,
        log_context="department"
    )


async def get_position_id(position: str) -> int:
    """
    Get the position ID for the employee.

    :param position: Position
    :return: Position ID from the position table.
    """
    return await fetch_parameter_id(
        base_path="get_position_id",
        identifier=position,
        log_context="position"
    )


async def fetch_employee_data(endpoint: str, identifier: str | int, log_context: str) -> pd.DataFrame | None:
    """
    Helper function to fetch employee data from API and return a DataFrame

    :param endpoint: API subpath
    :param identifier: Employee identifier
    :param log_context: Context for logging messages
    """
    logger.info(f"Initiating employee data retrieval process for {log_context}: {identifier} ...")
    url = f"{BASE_URL}/get_employee_data/{endpoint}/{identifier}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=HEADERS)

            if response.status_code == 404:
                logger.warning(f"Employee with {log_context} {identifier} not found.")
                return None

            response.raise_for_status()

            data = response.json()
            logger.info("Pandas Dataframe with employee data created.")
            return pd.DataFrame(data)

        except Exception as e:
            logger.error(f"Unexpected error occurred while retrieving data for employee {log_context} {identifier}: {e}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


async def get_employee_data_by_id(employee_id: int) -> pd.DataFrame | None:
    """Fetch employee data using employee id"""
    return await fetch_employee_data(
        endpoint="by_id",
        identifier=employee_id,
        log_context="ID"
    )


async def get_employee_data_by_first_name(first_name: str) -> pd.DataFrame | None:
    """Fetch employee data using their first name."""
    return await fetch_employee_data(
        endpoint="by_first_name",
        identifier=first_name,
        log_context="first name"
    )


async def get_employee_data_by_last_name(last_name: str) -> pd.DataFrame | None:
    """Fetch employee data using their last name."""
    return await fetch_employee_data(
        endpoint="by_last_name",
        identifier=last_name,
        log_context="last name"
    )


async def get_employee_data_by_department(department: str) -> pd.DataFrame | None:
    """Fetch employee data using their department."""
    return await fetch_employee_data(
        endpoint="by_department",
        identifier=department,
        log_context="department"
    )



async def add_new_user(
    role: str,
    firstname: str,
    lastname: str,
    dob: date,
    email: str,
    password: str,
    employee_id: int
) -> Dict[str, str]:
    """
    Add a new user to the user database for specified roles.

    User role: can only view employee data.
    Admin role: can perform all operations including addin, deleting and updating data.
    """
    logger.info("Initiating new user creating process ...")

    url = f"{BASE_URL}/add_user/"
    payload = {
        "role": role,
        "firstname": firstname,
        "lastname": lastname,
        "dob": dob.strftime("%Y-%m-%d"),
        "email": email,
        "password": password,
        "employee_id": employee_id,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()
        response = response.json()
        logger.info(f"{response.get('message')} with assigned role {role}")
        return response


async def add_new_employee_data(
    first_name: str,
    middle_name: str,
    last_name: str,
    address: str,
    date_of_birth: date,
    gender_id: int,
    phone: str,
    position_id: int,
    email: str,
    department_id: int,
    salary: int,
    hired_date: date,
    status: str = "Active",
) -> Dict[str, str]:  # type: ignore
    """
    Add a new employee details to the database.
    """
    logger.info(f"Initiating new employee creating process for {first_name} {last_name}...")

    url = f"{BASE_URL}/add_new_employee/"
    payload = {
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "address": address,
        "date_of_birth": date_of_birth.strftime("%Y-%m-%d"),
        "gender_id": gender_id,
        "phone": phone,
        "position_id": position_id,
        "department_id": department_id,
        "email": email,
        "salary": salary,
        "hired_date": hired_date.strftime("%Y-%m-%d"),
        "status": status,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload, headers=HEADERS)
            response.raise_for_status()
            response = response.json()

            if response.get("status") == "Success":
                logger.info(f"{response.get('message')}")
                return response
        except Exception as e:
            logger.error(f"Unexpected error occurred while adding employee data for {first_name} {last_name}: {e}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")



# TODO - Add new enpoint call for deleting employee data
# TODO - Add new enpoint call for updating employee data
