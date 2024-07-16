"""API endpoint module."""
from contextlib import asynccontextmanager
from typing import Any, AsyncContextManager, Dict

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import init_settings
from src.backend import db_connect, httpx_client


description = """
An API developed for the data retrieval and updates for the Employee Management System.

Developed and and managed by David Asogwa.

PS: This API is for this project purpose only.

📝[Source Code](https://github.com/Merci93/Employee-Management-System)
"""


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncContextManager[Any]:  # type: ignore
    # Startup
    init_settings()
    db_connect.user_db_init()
    httpx_client.init_httpx_client()
    yield
    # Shutdown
    db_connect.users_client.close()
    httpx_client.httpx_client.close()


app = FastAPI(
    title="Employee Data Retriever",
    docs_url="/",
    description=description,
    version="0.1",
    contact={
        "name": "David Asogwa",
        "contact": "https://github.com/Merci93/Employee-Management-System",
    },
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/root/v1/")
def get_root() -> dict[str, str]:
    """API root endpoint."""
    return {"message": "Hello!!! Root API running."}


@app.get("/verify_user/v1/")
def verify_user(username: str) -> Dict[str, Any]:
    """Verify user credentials in the database"""
    cursor = db_connect.users_client.cursor()
    cursor.execute("SELECT username, password FROM users WHERE username = %s", (username,))
    user_details = cursor.fetchall()
    if user_details:
        user_data = {"exist": True, "password": user_details[0][1]}
    else:
        user_data = {"exist": False, "password": None}
    return user_data


if __name__ == "__main__":
    uvicorn.run("api:app", port=8000, reload=True)
