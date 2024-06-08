import customtkinter as ctk
from PIL import Image


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.geometry("1230x678")
window.resizable(0, 0)
window.title("Login")
image = ctk.CTkImage(Image.open(r"./files/ems.png"), size=(1230, 678))
image_label = ctk.CTkLabel(window, image=image, text="")
image_label.place(x=0, y=0)
heading_label = ctk.CTkLabel(
    window, text="Employee Management System", bg_color="#7125FF",
    font=("Goudy Old Style", 60, "bold"),
)
heading_label.place(x=50, y=30)


window.mainloop()
