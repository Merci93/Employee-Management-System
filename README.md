# Employee Management System
An Employee Management System developed using Python, Customtkinter and tkinter libraries. The system is designed to include functionalities:
- Adding a new employee
- Updating employee data
- Deleting a specified employee data
- Deleting all data

The database is a PostgreSQL database and stores all employee information(s) including first name, last name, phone number, address, role, gender, department and salary.

The UI contains a query interface that displays the results when the database is queried for employee data.

### Overview
![](img/overview.png)

### Functionalities
1. **Login**: Verifies user login data against already existing data in the database. Access is granted if username exists. If username does not exists or password entered is wrong, an error message is shown. Dat verification in the database is possible via API endpoint.
2. **Add User**: Functionlaity to add a new user to the users database. This adds a new user detail via a FastAPI endpoint and will grant the specified user access to the Employee Management System. New user data includes username (which will be verified against the existing data in the database before being added), firstname, lastname, email and password (with a second confirmation).

### User Interface
>> TODO

### Setup
>> TODO
