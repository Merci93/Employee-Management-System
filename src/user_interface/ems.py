"""Employement Management System User Interface."""

import customtkinter
from PIL import Image


window = customtkinter.CTk()
window.geometry("1230x678")
window.resizable(False, False)
window.title("EMS")
window.configure(fg_color="#13132b")

image = customtkinter.CTkImage(Image.open(r"./files/ems_logo.jpg"), size=(330, 150))
image_label = customtkinter.CTkLabel(window, image=image, text="")
image_label.grid(row=0, column=0)

heading_label = customtkinter.CTkLabel(
    window,
    width=910,
    height=150,
    text="Employee Management System",
    text_color="black",
    bg_color="#F8992B",
    font=("Goudy Old Style", 68, "bold"),
)
heading_label.grid(row=0, column=1)

# Left frame
left_frame = customtkinter.CTkFrame(window, fg_color="#13132b")
left_frame.grid(row=1, column=0)

# Id
id_label = customtkinter.CTkLabel(left_frame, text="Id", font=("arial", 15, "bold"))
id_label.grid(row=0, column=0, padx=20, sticky="w")
id_value = customtkinter.CTkEntry(left_frame, font=("arial", 15, "bold"), width=180)
id_value.grid(row=0, column=1, pady=15, padx=(0, 20))

# Name
name_label = customtkinter.CTkLabel(left_frame, text="Name", font=("arial", 15, "bold"))
name_label.grid(row=1, column=0, padx=20, sticky="w")
name_value = customtkinter.CTkEntry(left_frame, font=("arial", 15, "bold"), width=180)
name_value.grid(row=1, column=1, pady=15, padx=(0, 20))

# Phone
phone_label = customtkinter.CTkLabel(left_frame, text="Phone", font=("arial", 15, "bold"))
phone_label.grid(row=2, column=0, padx=20, sticky="w")
phone_value = customtkinter.CTkEntry(left_frame, font=("arial", 15, "bold"), width=180)
phone_value.grid(row=2, column=1, pady=15, padx=(0, 20))

# Role
role_label = customtkinter.CTkLabel(left_frame, text="Role", font=("arial", 15, "bold"))
role_label.grid(row=3, column=0, padx=20, sticky="w")
roles = [
    "HR", "Data Engineer", "Solutions Architect", "Data Analyst", "Intern", "Business Analyst",
    "Senior Manager Engineering", "Data Scientist", "Junior Data Engineer", "Web Developer",
    "Cloud Architect", "Software Engineer", "Network Engineer", "Others"
]
role_value = customtkinter.CTkComboBox(
    left_frame, values=roles, font=("arial", 15, "bold"), width=180, state="readonly",
)
role_value.grid(row=3, column=1, pady=15, padx=(0, 20))
role_value.set("Select Role")

# Gender
gender_label = customtkinter.CTkLabel(left_frame, text="Gender", font=("arial", 15, "bold"))
gender_label.grid(row=4, column=0, padx=15, sticky="w")
gender = ["Male", "Female"]
gender_value = customtkinter.CTkComboBox(
    left_frame, values=gender, font=("arial", 15, "bold"), width=180, state="readonly",
)
gender_value.grid(row=4, column=1, pady=15, padx=(0, 20))
gender_value.set("Select gender")

# Department
department_label = customtkinter.CTkLabel(left_frame, text="Department", font=("arial", 15, "bold"))
department_label.grid(row=5, column=0, padx=20, sticky="w")
departments = ["IT", "Marketing", "Sales", "Research", "HR", "Others"]
department_value = customtkinter.CTkComboBox(
    left_frame, values=departments, font=("arial", 15, "bold"), width=180, state="readonly",
)
department_value.grid(row=5, column=1, pady=15, padx=(0, 20))

# Salary
salary_label = customtkinter.CTkLabel(left_frame, text="Salary", font=("arial", 15, "bold"))
salary_label.grid(row=6, column=0, padx=20, sticky="w")
salary_value = customtkinter.CTkEntry(left_frame, font=("arial", 15, "bold"), width=180)
salary_value.grid(row=6, column=1, pady=15, padx=(0, 20))

# right_frame = customtkinter.CTkFrame(window)
# right_frame.grid(row=1, column=1, columnspan=2)

window.mainloop()
