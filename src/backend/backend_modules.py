""""Backend module"""
from typing import Any, Dict

from src.backend import httpx_client


headers = {"accept": "application/json"}


def verify_user(username: str) -> Dict[str, Any]:
    """Verify user before login."""
    url = "http://localhost:8000/verify_user/v1/"
    params = {
        "username": username,
    }
    response = httpx_client.httpx_client.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def verify_email(email: str) -> Dict[str, Any]:
    """Verify email before creating user."""
    url = "http://localhost:8000/verify_email/v1/"
    params = {
        "email": email,
    }
    response = httpx_client.httpx_client.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()
