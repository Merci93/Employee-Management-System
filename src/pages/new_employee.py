import streamlit as st
import pandas as pd

# Initialize session state if not already present
if 'employees' not in st.session_state:
    cols = ["Id", "First Name", "Middle Name", "Last Name", "Date of Birth", "Gender", "Phone", "Role", "Department", "Salary"]
    st.session_state.employees = pd.DataFrame(columns=cols)

st.header("Add New Employee")
with st.form("add_employee_form"):
    emp_id = st.text_input("Id")
    first_name = st.text_input("First Name")
    middle_name = st.text_input("Middle Name")
    last_name = st.text_input("Last Name")
    dob = st.date_input("Date of Birth")
    gender = st.selectbox("Gender", ["Male", "Female"])
    phone = st.text_input("Phone")
    role = st.selectbox("Role", ["HR", "Data Engineer", "Solutions Architect", "Data Analyst", "Intern", "Business Analyst"])
    department = st.selectbox("Department", ["IT", "Marketing", "Sales", "Research", "HR", "Others", "Data & Analytics"])
    salary = st.text_input("Salary")
    submit_button = st.form_submit_button("Save")

if submit_button:
    new_data = pd.DataFrame([[emp_id, first_name, middle_name, dob, gender, last_name, phone, role, department, salary]],
                            columns=st.session_state.employees.columns)
    st.session_state.employees = pd.concat([st.session_state.employees, new_data], ignore_index=True)
    st.success("Employee added successfully!")
