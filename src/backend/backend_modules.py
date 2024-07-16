""""Backend module"""
from src.backend import httpx_client


def verify_user(username: str) -> None:
    """Verify user before login."""
    headers = {"accept": "application/json"}
    response = httpx_client.httpx_client.get(
        f"http://localhost:8000/verify_user/v1/?username={username}",
        headers=headers,
    )
    response.raise_for_status()
    return response.json()
