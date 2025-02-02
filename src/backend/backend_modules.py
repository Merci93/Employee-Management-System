""""Backend module"""
import datetime
from typing import Dict

from src.backend import httpx_client


headers = {"accept": "application/json"}


async def verify_username(username: str) -> bool:
    """
    Verify if username already exists in the user database..

    :param Username: Input username to check.
    return: A boolean True if it exists, False otherwise.
    """
    url = "http://localhost:8000/v1/verify_user/"
    params = {
        "username": username,
    }
    async with httpx_client.httpx_client as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json().get("exist", False)


async def verify_email(email: str) -> bool:
    """
    Verify if user email already exists in the database.

    :param Email: Input email to check.
    return: A boolean True if it exists, False otherwise.
    """
    url = "http://localhost:8000/v1/verify_email/"
    params = {
        "email": email,
    }
    async with httpx_client.httpx_client as client:
        response = await client.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json().get("exist", False)


async def add_new_user(
    role: str,
    username: str,
    firstname: str,
    lastname: str,
    dob: datetime.date,
    email: str,
    password: str,
) -> Dict[str, str]:
    """
    Add a new user to the user database for specified roles.

    User role: can only view employee data.
    Admin role: can perform all operations including addin, deleting and updating data.
    """
    url = "http://localhost:8000/v1/add_user/"
    data = {
        "username": username,
        "first_name": firstname,
        "last_name": lastname,
        "date_of_birth": dob.strftime("%Y-%m-%d"),
        "email": email,
        "role": role,
        "password": password,
    }
    async with httpx_client.httpx_client as client:
        response = await client.post(url, json=data, headers=headers, data={})
        response.raise_for_status()
        return response.json().get("exist", False)
