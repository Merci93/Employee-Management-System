"""Employement Management System User Interface."""
import tkinter

import customtkinter
from PIL import Image


window = customtkinter.CTk()
window.geometry("1230x678+22+9")
window.resizable(False, False)
window.title("EMS")
window.configure(fg_color="#13132b")

# Add header image
image = customtkinter.CTkImage(Image.open(r"./files/ems_logo.jpg"), size=(280, 150))
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
id_value = customtkinter.CTkEntry(left_frame, font=("arial", 15, "bold"), width=140)
id_value.grid(row=0, column=1, pady=12, padx=(0, 20))

# First Name
first_name_label = customtkinter.CTkLabel(left_frame, text="First Name", font=("arial", 15, "bold"))
first_name_label.grid(row=1, column=0, padx=20, sticky="w")
first_name_value = customtkinter.CTkEntry(left_frame, font=("arial", 15, "bold"), width=140)
first_name_value.grid(row=1, column=1, pady=12, padx=(0, 20))

# Last Name
last_name_label = customtkinter.CTkLabel(left_frame, text="Last Name", font=("arial", 15, "bold"))
last_name_label.grid(row=2, column=0, padx=20, sticky="w")
last_name_value = customtkinter.CTkEntry(left_frame, font=("arial", 15, "bold"), width=140)
last_name_value.grid(row=2, column=1, pady=12, padx=(0, 20))

# Phone
phone_label = customtkinter.CTkLabel(left_frame, text="Phone", font=("arial", 15, "bold"))
phone_label.grid(row=3, column=0, padx=20, sticky="w")
phone_value = customtkinter.CTkEntry(left_frame, font=("arial", 15, "bold"), width=140)
phone_value.grid(row=3, column=1, pady=12, padx=(0, 20))

# Role
role_label = customtkinter.CTkLabel(left_frame, text="Role", font=("arial", 15, "bold"))
role_label.grid(row=4, column=0, padx=20, sticky="w")
roles = [
    "HR", "Data Engineer", "Solutions Architect", "Data Analyst", "Intern", "Business Analyst",
    "Senior Manager Engineering", "Data Scientist", "Junior Data Engineer", "Web Developer",
    "Cloud Architect", "Software Engineer", "Network Engineer", "Others"
]
role_value = customtkinter.CTkComboBox(
    left_frame, values=roles, font=("arial", 15, "bold"), width=140, state="readonly",
)
role_value.grid(row=4, column=1, pady=12, padx=(0, 20))
role_value.set("Select Role")

# Gender
gender_label = customtkinter.CTkLabel(left_frame, text="Gender", font=("arial", 15, "bold"))
gender_label.grid(row=5, column=0, padx=20, sticky="w")
gender = ["Male", "Female"]
gender_value = customtkinter.CTkComboBox(
    left_frame, values=gender, font=("arial", 15, "bold"), width=140, state="readonly",
)
gender_value.grid(row=5, column=1, pady=12, padx=(0, 20))
gender_value.set("Select gender")

# Department
department_label = customtkinter.CTkLabel(left_frame, text="Department", font=("arial", 15, "bold"))
department_label.grid(row=6, column=0, padx=20, sticky="w")
departments = ["IT", "Marketing", "Sales", "Research", "HR", "Others"]
department_value = customtkinter.CTkComboBox(
    left_frame, values=departments, font=("arial", 15, "bold"), width=140, state="readonly",
)
department_value.grid(row=6, column=1, pady=12, padx=(0, 20))

# Salary
salary_label = customtkinter.CTkLabel(left_frame, text="Salary", font=("arial", 15, "bold"))
salary_label.grid(row=7, column=0, padx=20, sticky="w")
salary_value = customtkinter.CTkEntry(left_frame, font=("arial", 15, "bold"), width=140)
salary_value.grid(row=7, column=1, pady=12, padx=(0, 20))

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
search_entry = customtkinter.CTkEntry(right_frame, width=200)
search_entry.grid(row=0, column=1)

# Search Button
search_button = customtkinter.CTkButton(right_frame, text="Search", width=100)
search_button.grid(row=0, column=2)

# Show all button
show_all = customtkinter.CTkButton(right_frame, text="Show All Results")
show_all.grid(row=0, column=3)

# Results Treeview Window
results_window = tkinter.ttk.Treeview(right_frame, height=18)
results_window.grid(row=1, column=0, columnspan=4)
results_window["columns"] = ("Id", "Name", "Phone", "Role", "Gender", "Department", "Salary")
results_window_map = ("Id", "Name", "Phone", "Role", "Gender", "Department", "Salary")
for item in results_window_map:
    results_window.heading(item, text=item)
results_window.config(show="headings")

results_window_size = {"Id": 120,
                       "Name": 200,
                       "Phone": 140,
                       "Role": 150,
                       "Gender": 100,
                       "Department": 180,
                       "Salary": 150,
                       }
for key, value in results_window_size.items():
    results_window.column(key, width=value)
tkinter.ttk.Style().configure("Treeview.Heading", font=("arial", 18, "bold"))

window.mainloop()
