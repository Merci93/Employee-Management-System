"""
A module for defining Pydantic models and Enums for validating input data in API endpoints.
This module includes Pydantic models for employee creation and update requests, as well as Enums
for validating specific fields such as department, gender, and position. The models ensure that
incoming data adheres to the expected structure and types, while the Enums restrict values to
predefined options, enhancing data integrity and consistency across the application.
"""
from datetime import date
from enum import Enum

from pydantic import BaseModel


class DepartmentIdRequest(str, Enum):
    it = "IT"
    hr = "HR"
    sales = "Sales"
    research = "Research"
    marketing = "Marketing"
    data_analytics = "Data & Analytics"


class EmployeeCreateRequest(BaseModel):
    phone: str
    email: str
    status: str
    address: str
    salary: float
    gender_id: int
    last_name: str
    first_name: str
    hired_date: str
    position_id: int
    middle_name: str
    date_of_birth: str
    department_id: int


class EmployeeResponseModel(BaseModel):
    id: int
    email: str
    phone: str
    gender: str
    status: str
    address: str
    position: str
    salary: float
    last_name: str
    department: str
    first_name: str
    hired_date: date
    date_of_birth: date
    middle_name: str | None = None
    date_resigned: date | None = None


class EmployeeUpdateRequest(BaseModel):
    employee_id: int
    address: str | None = None
    salary: int | float | None = None
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    position_id: int | None = None
    department_id: int | None = None
    phone: str | None = None


class GenderIdRequest(str, Enum):
    male = "Male"
    female = "Female"


class PositionIdRequest(str, Enum):
    hr = "HR"
    intern = "Intern"
    data_analyst = "Data Analyst"
    data_engineer = "Data Engineer"
    product_owner = "Product Owner"
    web_developer = "Web Developer"
    data_scientist = "Data Scientist"
    devops_engineer = "DevOps Engineer"
    cloud_architect = "Cloud Architect"
    network_engineer = "Network Engineer"
    business_analyst = "Business Analyst"
    software_engineer = "Software Engineer"
    jnr_data_eengieer = "Junior Data Engineer"
    solutions_architect = "Solutions Architect"
    senior_engr_mgr = "Senior Engineering Manager"


class WhoToVerify(str, Enum):
    admin = "admin"
    manager = "manager"
    employee = "employee"