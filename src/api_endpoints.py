"""API endpoint module."""
from contextlib import asynccontextmanager
from typing import Any, AsyncContextManager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import init_settings
from src.backend import db_connect


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
    yield
    # Shutdown
    db_connect.users_client.close()


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
def verify_user(username: str) -> bool:
    """Verify user credentials in the database"""
    cursor = db_connect.users_client.cursor()
    cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
    user = cursor.fetchall()
    return True if user else False


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
