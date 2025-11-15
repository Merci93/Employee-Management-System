import streamlit as st
import pandas as pd


# Markdown ro center headings
st.markdown("""
    <style>
    h1, h2, h3 {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state if not already present
if 'employees' not in st.session_state:
    cols = ["Id", "First Name", "Middle Name", "Last Name", "Date of Birth", "Gender", "Phone", "Role", "Department", "Salary"]
    st.session_state.employees = pd.DataFrame(columns=cols)

st.header("Delete Employee Data")
emp_id = st.text_input("Enter Employee ID to Delete")
if st.button("Delete Employee", key="delete_button", help="This action is irreversible!", use_container_width=True):
    confirm = st.warning("This action is irreversible. Do you want to delete this employee?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes"):
            st.session_state.employees = st.session_state.employees[st.session_state.employees["Id"] != emp_id]
            st.success("Employee deleted successfully!")
    with col2:
        if st.button("No"):
            st.info("Deletion canceled")
