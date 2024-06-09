"""Employement Management System User Interface."""

import customtkinter
from PIL import Image


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

window = customtkinter.CTk()
window.geometry("1230x678")
window.resizable(False, False)
window.title("EMS")

image = customtkinter.CTkImage(Image.open(r"./files/ems_logo.jpg"), size=(300, 150))
image_label = customtkinter.CTkLabel(window, image=image, text="")
image_label.grid(row=0, column=0)

heading_label = customtkinter.CTkLabel(
    window,
    width=930,
    height=150,
    text="Employee Management System",
    text_color="black",
    bg_color="#F8992B",
    font=("Goudy Old Style", 68, "bold"),
)
heading_label.grid(row=0, column=1)

left_frame = customtkinter.CTkFrame(window)
left_frame.grid(row=1, column=0)

id_label = customtkinter.CTkLabel(left_frame, text="Id", font=("arial", 15, "bold"))
id_label.grid(row=0, column=0, padx=20, sticky="w")
id_value = customtkinter.CTkEntry(left_frame, font=("arial", 15, "bold"), width=180)
id_value.grid(row=0, column=1, pady=20)

name_label = customtkinter.CTkLabel(left_frame, text="Name", font=("arial", 15, "bold"))
name_label.grid(row=1, column=0, padx=20, sticky="w")
name_value = customtkinter.CTkEntry(left_frame, font=("arial", 15, "bold"), width=180)
name_value.grid(row=1, column=1, pady=20)


window.mainloop()
