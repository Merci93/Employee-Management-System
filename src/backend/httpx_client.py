"""HTTPX client module."""
import httpx


def init_httpx_client() -> None:
    """Initialize httpx client."""
    global httpx_client
    httpx_client = httpx.Client()


httpx_client = None
if not httpx_client:
    init_httpx_client()
