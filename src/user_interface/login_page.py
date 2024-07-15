"""Employee Management System Login Page."""
import sys
from tkinter import messagebox

import customtkinter
from PIL import Image

sys.path.append(".")

from src.backend import backend_modules
from src.user_interface import add_new_user, ems


def verify_credentials(username: str, password: str) -> bool:
    """Verify user credentials."""
    user_data = backend_modules.verify_user(username)
    if user_data.get("exist") and user_data.get("password") == password:
        return True
    return False


def login() -> None:
    """Login page."""

    def get_username_ui() -> None:
        """Get username from login interface."""
        username = username_entry.get()
        input_password = password_entry.get()

        if not username or not input_password:
            messagebox.showerror("Error", "Username and Password fields are required.")
            return

        if verify_credentials(username, input_password):
            global logged_in
            logged_in = True
            login_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid Username or Password.")

    login_window = customtkinter.CTk()
    login_window.geometry("1130x578+100+80")
    login_window.resizable(0, 0)
    login_window.title("Login")

    image = customtkinter.CTkImage(Image.open(r"./img/login_image.png"), size=(1138, 578))
    image_label = customtkinter.CTkLabel(login_window, image=image, text="")
    image_label.place(x=0, y=0)

    heading_label = customtkinter.CTkLabel(
        login_window, text="Employee Management System", bg_color="#7125FF",
        font=("Goudy Old Style", 60, "bold"),
    )
    heading_label.place(x=50, y=30)

    username_entry = customtkinter.CTkEntry(
        login_window,
        width=180,
        placeholder_text="Enter Username",
        border_color="#7125FF",
        bg_color="#7125FF",
    )
    username_entry.place(x=150, y=200)

    password_entry = customtkinter.CTkEntry(
        login_window,
        width=180,
        placeholder_text="Password",
        show="*",
        border_color="#7125FF",
        bg_color="#7125FF",
    )
    password_entry.place(x=150, y=250)

    login_button = customtkinter.CTkButton(
        login_window,
        text="Login",
        cursor="hand2",
        bg_color="#7125FF",
        width=100,
        command=get_username_ui,
    )
    login_button.place(x=190, y=300)

    create_user_button = customtkinter.CTkButton(
        login_window,
        text="Create New User",
        cursor="hand2",
        bg_color="#7125FF",
        width=100,
        command=add_new_user.new_user,
    )
    create_user_button.place(x=183, y=400)

    login_window.mainloop()


if __name__ == "__main__":
    global logged_in
    logged_in = False
    login()

    if logged_in:
        ems.user_interface()
