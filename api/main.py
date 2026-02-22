"""API endpoint main"""
from typing import Any, AsyncContextManager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.endpoints.root import root_router
from api.endpoints.verification import verification_router
from api.endpoints.ids import id_router
# from api.endpoints.users import router as users_router
from api.endpoints.employees import employees_data_router
from api.endpoints.updates import updates_router
from app.config.config import init_settings
from api.endpoints.new_employee import router as add_new_employee_router
# from log_handler import logger
from backend import db_connect


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
            "name": "Employee Email and Phone Number Verification",
            "description": "Endpoints for verifying employee data - email, phone number and ID.",
        },
        {
            "name": "ID Retrieval",
            "description": "Endpoints for retrieving id for specified gender, department and position from their respective tables.",
        },
        {
            "name": "Admin and User Management",
            "description": "Endpoints to add employees as user and admins in order to access or modify data.",
        },
        {
            "name": "Add New Employee",
            "description": "Endpoints to add new employee data to the database.",
        },
        {
            "name": "Employee Data",
            "description": "Endpoints to retrieve employee data based on specified criteria.",
        },
        {
            "name": "Update Employee Data",
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
app.include_router(id_router)
app.include_router(root_router)
app.include_router(updates_router)
app.include_router(employees_data_router)
app.include_router(verification_router)
app.include_router(add_new_employee_router)
