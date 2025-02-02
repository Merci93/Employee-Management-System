""""Backend module"""
from typing import Any, Dict

from src.backend import httpx_client


headers = {"accept": "application/json"}


def verify_username(username: str) -> Dict[str, Any]:
    """Verify username."""
    url = "http://localhost:8000/verify_user/v1/"
    params = {
        "username": username,
    }
    response = httpx_client.httpx_client.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def verify_email(email: str) -> Dict[str, Any]:
    """Verify user email."""
    url = "http://localhost:8000/verify_email/v1/"
    params = {
        "email": email,
    }
    response = httpx_client.httpx_client.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def add_new_user(username: str, firstname: str, lastname: str, email: str, password: str) -> Dict[str, str]:
    """Add a new user to the database."""
    url = "http://localhost:8000/add_user/v1/"
    params = {
        "username": username,
        "first_name": firstname,
        "last_name": lastname,
        "email": email,
        "password": password,
    }
    response = httpx_client.httpx_client.post(url, params=params, headers=headers, data={})
    response.raise_for_status()
    return response.json()
