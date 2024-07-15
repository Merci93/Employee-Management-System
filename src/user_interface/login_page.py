"""Employee Management System Login Page."""
import customtkinter
from PIL import Image

from user_interface.add_new_user import new_user


def login() -> None:
    """Login page"""
    window = customtkinter.CTk()
    window.geometry("1130x578+100+80")
    window.resizable(0, 0)
    window.title("Login")

    image = customtkinter.CTkImage(Image.open(r"./img/login_image.png"), size=(1138, 578))
    image_label = customtkinter.CTkLabel(window, image=image, text="")
    image_label.place(x=0, y=0)

    heading_label = customtkinter.CTkLabel(
        window, text="Employee Management System", bg_color="#7125FF",
        font=("Goudy Old Style", 60, "bold"),
    )
    heading_label.place(x=50, y=30)

    username_entry = customtkinter.CTkEntry(
        window,
        width=180,
        placeholder_text="Enter Username",
        border_color="#7125FF",
        bg_color="#7125FF",
    )
    username_entry.place(x=150, y=200)

    password_entry = customtkinter.CTkEntry(
        window,
        width=180,
        placeholder_text="Password",
        show="*",
        border_color="#7125FF",
        bg_color="#7125FF",
    )
    password_entry.place(x=150, y=250)

    login_button = customtkinter.CTkButton(
        window,
        text="Login",
        cursor="hand2",
        bg_color="#7125FF",
        width=100,
    )
    login_button.place(x=190, y=300)

    create_user_button = customtkinter.CTkButton(
        window,
        text="Create New user",
        cursor="hand2",
        bg_color="#7125FF",
        width=100,
        command=new_user,
    )
    create_user_button.place(x=183, y=400)

    window.mainloop()
