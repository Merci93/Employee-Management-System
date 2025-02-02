"""HTTPX client module."""
import httpx


httpx_client: httpx.AsyncClient = None


def init_httpx_client() -> None:
    """Initialize async HTTPX client."""
    global httpx_client
    if httpx_client is None:
        httpx_client = httpx.AsyncClient()


async def close_httpx_client() -> None:
    """Properly close the HTTPX client to release resources."""
    global httpx_client
    if httpx_client is not None:
        await httpx_client.aclose()
        httpx_client = None


# Initialize the client when the module is loaded
init_httpx_client()
