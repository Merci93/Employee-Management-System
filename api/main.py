"""API endpoint main"""
from typing import Any, AsyncContextManager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.api.root import router as root_router
from src.api.verification import router as verification_router
from src.api.ids import router as ids_router
# from src.api.users import router as users_router
from src.api.employees import router as employees_router
from src.api.updates import router as updates_router

from src.backend import db_connect
from src.config import init_settings
# from src.log_handler import logger


description = """
An API developed for the data retrieval and updates for the Employee Management System.

Developed and and managed by David Asogwa.

PS: This API is for this project purpose only.

📝[Source Code](https://github.com/Merci93/Employee-Management-System)
"""


@asynccontextmanager  # type: ignore
async def lifespan(app: FastAPI) -> AsyncContextManager[Any]:  # type: ignore
    # Startup
    init_settings()
    db_connect.db_init()
    yield  # type: ignore
    db_connect.db_client.close()


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
    openapi_tags=[
        {
            "name": "Employee Data Verification",
            "description": "Endpoints for verifying employee data - email, phone number and ID.",
        },
        {
            "name": "Retrieve ID",
            "description": "Endpoints for retrieving id for specified gender, department and position from their respective tables.",
        },
        {
            "name": "Admin and User Management",
            "description": "Endpoints to add employees as user and admins in order to access or modify data.",
        },
        {
            "name": "Employee Management",
            "description": "Endpoints to manage employee data - add, update and delete.",
        },
        {
            "name": "Employee Data Search",
            "description": "Endpoints to fetch employee data.",
        },
        {
            "name": "Employee Data Update",
            "description": "Endpoints to update employee data.",
        },
    ],
)


app.add_middleware(
    CORSMiddleware,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Register all router modules
app.include_router(ids_router)
app.include_router(root_router)
app.include_router(updates_router)
app.include_router(employees_router)
app.include_router(verification_router)
