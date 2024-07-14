"""Employement Management System User Interface."""
import tkinter

import customtkinter
from PIL import Image


def user_interface() -> None:
    """EMS User Interface."""

    def add_switch() -> None:
        """Helper function for add button state."""
        if save_employee["state"] == "normal":
            save_employee["state"] = "disabled"
            update_employee["state"] = "disabled"
            enable_add_employee["text"] = "Enable Add/Update"
            id_value["state"] = "normal"
        else:
            save_employee["state"] = "normal"
            update_employee["state"] = "normal"
            enable_add_employee["text"] = "Disable Add/Update"

    def delete_switch() -> None:
        """Helper function for delete button state."""
        if delete_employee["state"] == "normal":
            delete_employee["state"] = "disabled"
            delete_all["state"] = "disabled"
            enable_delete_employee["text"] = "Enable Delete"
        else:
            delete_employee["state"] = "normal"
            delete_all["state"] = "normal"
            enable_delete_employee["text"] = "Disable Delete"

    window = customtkinter.CTk()
    window.geometry("1230x678+22+9")
    window.resizable(False, False)
    window.title("EMS")
    window.configure(fg_color="#13132b")

    # Add header image
    image = customtkinter.CTkImage(Image.open(r"./img/ems_logo.jpg"), size=(290, 150))
    image_header = customtkinter.CTkLabel(window, image=image, text="")
    image_header.grid(row=0, column=0)

    # Add header title
    heading_title = customtkinter.CTkLabel(
        window,
        width=980,
        height=150,
        text="Employee Management System",
        text_color="black",
        bg_color="#F8992B",
        font=("Goudy Old Style", 68, "bold"),
    )
    heading_title.grid(row=0, column=1)

    # Left frame
    left_frame = customtkinter.CTkFrame(window, fg_color="#13132b")
    left_frame.grid(row=1, column=0)

    # Id
    id_label = customtkinter.CTkLabel(left_frame, text="Id", font=("arial", 15, "bold"))
    id_label.grid(row=0, column=0, padx=20, sticky="w")
    id_value = customtkinter.CTkEntry(
        left_frame,
        font=("arial", 15, "bold"),
        placeholder_text="Enter Id",
        width=140,
    )
    id_value.grid(row=0, column=1, pady=9, padx=(0, 20))

    # First Name
    first_name_label = customtkinter.CTkLabel(
        left_frame,
        text="First Name",
        font=("arial", 15, "bold"),
    )
    first_name_label.grid(row=1, column=0, padx=20, sticky="w")
    first_name_value = customtkinter.CTkEntry(
        left_frame,
        font=("arial", 15, "bold"),
        placeholder_text="First Name",
        width=140,
    )
    first_name_value.grid(row=1, column=1, pady=9, padx=(0, 20))

    # Middle Name
    middle_name_label = customtkinter.CTkLabel(
        left_frame,
        text="Middle Name",
        font=("arial", 15, "bold"),
    )
    middle_name_label.grid(row=2, column=0, padx=20, sticky="w")
    middle_name_value = customtkinter.CTkEntry(
        left_frame,
        font=("arial", 15, "bold"),
        placeholder_text="Middle Name",
        width=140,
    )
    middle_name_value.grid(row=2, column=1, pady=9, padx=(0, 20))

    # Last Name
    last_name_label = customtkinter.CTkLabel(
        left_frame,
        text="Last Name",
        font=("arial", 15, "bold"),
    )
    last_name_label.grid(row=3, column=0, padx=20, sticky="w")
    last_name_value = customtkinter.CTkEntry(
        left_frame,
        font=("arial", 15, "bold"),
        placeholder_text="Last Name",
        width=140,
    )
    last_name_value.grid(row=3, column=1, pady=9, padx=(0, 20))

    # Phone
    phone_label = customtkinter.CTkLabel(left_frame, text="Phone", font=("arial", 15, "bold"))
    phone_label.grid(row=4, column=0, padx=20, sticky="w")
    phone_value = customtkinter.CTkEntry(
        left_frame,
        font=("arial", 15, "bold"),
        placeholder_text="Phone",
        width=140,
    )
    phone_value.grid(row=4, column=1, pady=9, padx=(0, 20))

    # Role
    role_label = customtkinter.CTkLabel(left_frame, text="Role", font=("arial", 15, "bold"))
    role_label.grid(row=5, column=0, padx=20, sticky="w")
    roles = [
        "HR", "Data Engineer", "Solutions Architect", "Data Analyst", "Intern", "Business Analyst",
        "Senior Manager Engineering", "Data Scientist", "Junior Data Engineer", "Web Developer",
        "Cloud Architect", "Software Engineer", "Network Engineer", "DevOps Engineer",
        "Product Owner", "Others",
    ]
    role_value = customtkinter.CTkComboBox(
        left_frame, values=roles, font=("arial", 15, "bold"), width=140, state="readonly",
    )
    role_value.grid(row=5, column=1, pady=9, padx=(0, 20))
    role_value.set("Select Role")

    # Gender
    gender_label = customtkinter.CTkLabel(left_frame, text="Gender", font=("arial", 15, "bold"))
    gender_label.grid(row=6, column=0, padx=20, sticky="w")
    gender = ["Male", "Female"]
    gender_value = customtkinter.CTkComboBox(
        left_frame, values=gender, font=("arial", 15, "bold"), width=140, state="readonly",
    )
    gender_value.grid(row=6, column=1, pady=9, padx=(0, 20))
    gender_value.set("Select Gender")

    # Department
    department_label = customtkinter.CTkLabel(
        left_frame,
        text="Department",
        font=("arial", 15, "bold"),
    )
    department_label.grid(row=7, column=0, padx=20, sticky="w")
    departments = ["IT", "Marketing", "Sales", "Research", "HR", "Others"]
    department_value = customtkinter.CTkComboBox(
        left_frame, values=departments, font=("arial", 15, "bold"), width=140, state="readonly",
    )
    department_value.grid(row=7, column=1, pady=9, padx=(0, 20))
    department_value.set("Select Dept.")

    # Salary
    salary_label = customtkinter.CTkLabel(left_frame, text="Salary", font=("arial", 15, "bold"))
    salary_label.grid(row=8, column=0, padx=20, sticky="w")
    salary_value = customtkinter.CTkEntry(
        left_frame,
        font=("arial", 15, "bold"),
        placeholder_text="Salary",
        width=140,
    )
    salary_value.grid(row=8, column=1, pady=9, padx=(0, 20))

    # Right frame
    right_frame = customtkinter.CTkFrame(window)
    right_frame.grid(row=1, column=1, columnspan=2)

    # Search Options
    options = ["Id", "Name", "Phone", "Role", "Gender", "Department", "Salary"]
    search_value = customtkinter.CTkComboBox(
        right_frame, values=options, font=("arial", 15, "bold"), width=140, state="readonly",
    )
    search_value.grid(row=0, column=0, pady=10)
    search_value.set("Search By")

    # Search Entry
    search_entry = customtkinter.CTkEntry(
        right_frame,
        placeholder_text="Search Criteria",
        width=200,
    )
    search_entry.grid(row=0, column=1)

    # Search Button
    search_button = tkinter.Button(
        right_frame,
        text="Search",
        font=("aria", 15, "bold"),
        width=15,
        height=0,
        background="#1E66A4",
        foreground="#ffffff",
        cursor="hand2",
        )
    search_button.grid(row=0, column=2)

    # Show all button
    show_all = tkinter.Button(
        right_frame,
        text="Show All Results",
        font=("aria", 15, "bold"),
        width=15,
        height=0,
        background="#1E66A4",
        foreground="#ffffff",
        cursor="hand2",
        )
    show_all.grid(row=0, column=3)

    # Results Treeview Window
    results_window = tkinter.ttk.Treeview(right_frame, height=18)
    results_window.grid(row=1, column=0, columnspan=4)
    results_window["columns"] = ("Id", "Name", "Phone", "Role", "Gender", "Department", "Salary")
    results_window_map = ("Id", "Name", "Phone", "Role", "Gender", "Department", "Salary")
    for item in results_window_map:
        results_window.heading(item, text=item)
    results_window.config(show="headings")

    results_window_size = {
        "Id": 120,
        "Name": 200,
        "Phone": 140,
        "Role": 150,
        "Gender": 100,
        "Department": 180,
        "Salary": 150,
    }
    for key, value in results_window_size.items():
        results_window.column(key, width=value)
    style = tkinter.ttk.Style()
    style.configure("Treeview.Heading", font=("arial", 18, "bold"))
    style.configure("Treeview", font=("arial", 15, "bold"), rowheight=25)

    # Scroll bar
    scroll_bar = tkinter.ttk.Scrollbar(right_frame, orient="vertical")
    scroll_bar.grid(row=1, column=4, sticky="ns")

    # Button Frame Functionalities
    button_frame = customtkinter.CTkFrame(window, fg_color="#13132b")
    button_frame.grid(row=2, column=0, columnspan=2)

    # Enable/Disable Add New Employee Data
    enable_add_employee = tkinter.Button(
        button_frame,
        text="Enable Add/Update",
        font=("aria", 15, "bold"),
        width=20,
        background="#1E66A4",
        foreground="#ffffff",
        cursor="hand2",
        command=add_switch,
    )
    enable_add_employee.grid(row=0, column=0, pady=40, padx=(20, 0))

    # Save Employee Data
    save_employee = tkinter.Button(
        button_frame,
        text="Save Employee Data",
        font=("aria", 15, "bold"),
        width=20,
        background="#1E66A4",
        foreground="#ffffff",
        cursor="hand2",
        state="disabled"
    )
    save_employee.grid(row=0, column=1, pady=40, padx=(10, 0))

    # Update Employee Data
    update_employee = tkinter.Button(
        button_frame,
        text="Update Employee Data",
        font=("aria", 15, "bold"),
        width=20,
        background="#1E66A4",
        foreground="#ffffff",
        cursor="hand2",
        state="disabled"
    )
    update_employee.grid(row=0, column=2, pady=40, padx=(10, 0))

    # Enable/Disable Delete Employee Data
    enable_delete_employee = tkinter.Button(
        button_frame,
        text="Enable Delete",
        font=("aria", 15, "bold"),
        width=20,
        background="#1E66A4",
        foreground="red",
        cursor="hand2",
        command=delete_switch,
    )
    enable_delete_employee.grid(row=0, column=3, pady=40, padx=(10, 0))

    # Delete Employee Data
    delete_employee = tkinter.Button(
        button_frame,
        text="Delete Employee Data",
        font=("aria", 15, "bold"),
        width=20,
        background="#1E66A4",
        foreground="red",
        cursor="hand2",
        state="disabled"
    )
    delete_employee.grid(row=0, column=4, pady=40, padx=(10, 0))

    # Delete All
    delete_all = tkinter.Button(
        button_frame,
        text="Delete All",
        font=("aria", 15, "bold"),
        width=20,
        background="#1E66A4",
        foreground="red",
        cursor="hand2",
        state="disabled"
    )
    delete_all.grid(row=0, column=5, pady=40, padx=(10, 0))

    window.mainloop()
