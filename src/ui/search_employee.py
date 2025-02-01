import streamlit as st
import pandas as pd

# Initialize session state if not already present
if 'employees' not in st.session_state:
    cols = ["Id", "First Name", "Middle Name", "Last Name", "Date of Birth", "Gender", "Phone", "Role", "Department", "Salary"]
    st.session_state.employees = pd.DataFrame(columns=cols)

st.header("Search Employee")
search_option = st.selectbox("Search by", ["First Name", "Last Name", "Employee ID", "Department"])
search_query = st.text_input("Enter search query")
if st.button("Search"):
    pass  # Placeholder for search functionality
st.dataframe(st.session_state.employees)
