import streamlit as st


# Markdown to center headings
st.markdown("""
    <style>
    h1, h2, h3 {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# User role obtained from database after login, but for now, we will define them
if "role" not in st.session_state:
    st.session_state.role = None


def login():

    st.header("Log in")

    # Inputs
    email_or_id = st.text_input("Employee ID or Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["Admin", "User"])

    # Login Button
    if st.button("Log in"):
        if email_or_id and password:
            # TODO Add backemd call for password and email or id verification
            # Call Backend API to fetch password and verify user
            if role == "Admin":
                st.session_state.role = "Admin"
                st.success("Login Successful!")
                st.rerun()
            elif role == "User":
                st.session_state.role = "User"
                st.success("Login Successful!")
                st.rerun()
            else:
                st.error("Invalid credentials or role.")
        else:
            st.warning("Please enter both email and password.")


def logout():
    st.session_state.role = None
    st.rerun()


role = st.session_state.role

# Define pages with icons and titles
logout_page = st.Page(
    logout,
    title="Log out",
    icon=":material/logout:",
)

new_admin_user = st.Page(
    "ui/new_admin_user.py",
    title="Create New User",
    icon=":material/person_add:",
    default=(role == "admin"),
)

# new_admin = st.Page(
#     "ui/new_admin.py",
#     title="Create New Admin",
#     icon=":material/person_add:",
#     default=(role == "admin"),
# )

search_employees = st.Page(
    "ui/search_employee.py",
    title="Search",
    icon=":material/search:",
)

add_employee = st.Page(
    "ui/new_employee.py",
    title="New Employee",
    icon=":material/person_add:",
    default=(role == "admin"),
)

update_employee = st.Page(
    "ui/update_employee_data.py",
    title="Update Employee Data",
    icon=":material/edit:",
    default=(role == "admin"),
)

delete_employee = st.Page(
    "ui/delete_employee_data.py",
    title="Delete Employee Data",
    icon=":material/delete_forever:",
    default=(role == "admin"),
)

user_details = st.Page(
    "ui/user_details.py",
    title="User Details",
    icon=":material/person:",
)

st.title("Employee Management System")
st.logo("img/ems_logo.jpg", icon_image="img/CustomTkinter_icon_Windows.ico")

account_pages = [user_details, logout_page]
user_pages = [search_employees]
admin_pages = [search_employees, add_employee, update_employee, delete_employee]
create_user_pages = [new_admin_user]

page_dict = {}
if role is not None and role.lower() == "user":
    page_dict["Logged in as User"] = user_pages
if role is not None and role.lower() == "admin":
    page_dict["Logged in as Admin"] = admin_pages
    page_dict["Admins"] = create_user_pages

if len(page_dict) > 0:
    pages = st.navigation({"Account": account_pages} | page_dict)
else:
    pages = st.navigation([st.Page(login)])

pages.run()
