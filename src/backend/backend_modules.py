""""Backend module"""
import datetime
from typing import Any, Dict

from src.backend import httpx_client


headers = {"accept": "application/json"}


def verify_username(username: str) -> Dict[str, Any]:
    """Verify username."""
    url = "http://localhost:8000/v1/verify_user/"
    params = {
        "username": username,
    }
    response = httpx_client.httpx_client.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def verify_email(email: str) -> Dict[str, Any]:
    """Verify user email."""
    url = "http://localhost:8000/v1/verify_email/"
    params = {
        "email": email,
    }
    response = httpx_client.httpx_client.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def add_new_user(
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
    params = {
        "username": username,
        "first_name": firstname,
        "last_name": lastname,
        "date_of_birth": dob,
        "email": email,
        "role": role,
        "password": password,
    }
    response = httpx_client.httpx_client.post(url, params=params, headers=headers, data={})
    response.raise_for_status()
    return response.json()
