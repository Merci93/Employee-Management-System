""""Backend module"""
from datetime import date
from typing import Dict

import httpx

from src.log_handler import logger

BASE_URL = "http://localhost:8000/v1"
HEADERS = {"accept": "application/json"}


async def verify_username(username: str) -> bool:
    """
    Verify if username already exists in the user database..

    :param Username: Input username to check.
    return: A boolean True if it exists, False otherwise.
    """
    logger.info("Starting username verification...")

    url = f"{BASE_URL}/verify_username/"
    params = {
        "username": username,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=HEADERS)
        response.raise_for_status()
        logger.info("Username verification completed.")
        return response.json().get("exist", False)


async def verify_email(email: str) -> bool:
    """
    Verify if user email already exists in the database.

    :param Email: Input email to check.
    return: A boolean True if it exists, False otherwise.
    """
    logger.info("Starting email verification...")

    url = f"{BASE_URL}/verify_email/"
    params = {
        "email": email,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=HEADERS)
        response.raise_for_status()
        logger.info("Email verification completed.")
        return response.json().get("exist", False)


async def add_new_user(
    role: str,
    username: str,
    firstname: str,
    lastname: str,
    dob: date,
    email: str,
    password: str,
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
        "username": username,
        "firstname": firstname,
        "lastname": lastname,
        "dob": dob.strftime("%Y-%m-%d"),
        "email": email,
        "password": password,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()
        response = response.json()
        logger.info(f"{response.get('message')} with assigned role {role}")
        return response
