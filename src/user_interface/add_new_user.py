"""Module to create a new user."""
import sys
from tkinter import messagebox

import customtkinter

sys.path.append(".")

from src.backend import backend_modules


def verify_username(username: str) -> bool:
    """Verify if username already exists"""
    user_data = backend_modules.verify_user(username)
    if user_data.get("exist"):
        return True
    return False


def verify_email(email: str) -> bool:
    """Verify if email already exists"""
    user_data = backend_modules.verify_email(email)
    if user_data.get("exist"):
        return True
    return False


class NewUserWindow:
    def __init__(self) -> None:
        self.window = None

    def on_closing(self) -> None:
        """Close UI."""
        self.window.destroy()
        self.window = None

    def open_window(self) -> None:
        """Open Window."""

        def add_user() -> None:
            """verify user credentials and add to database if all tests passed."""
            fields = {
                "Username": new_username_entry.get(),
                "First Name": new_firstname_entry.get(),
                "Last Name": new_lastname_entry.get(),
                "Email": new_email_entry.get(),
                "Password": new_password_entry.get(),
                "Confirm Password": confirm_password_entry.get(),
            }

            missing_fields = [field_name for field_name, value in fields.items() if not value]

            if missing_fields:
                missing_required_fields = ", ".join(missing_fields)
                messagebox.showerror("Error", f"The following fields are required: {missing_required_fields}")
                return

            if verify_username(fields.get("Username")):
                messagebox.showerror("Error", f"Username {fields.get('Username')} already exists.")
                return

            if verify_email(fields.get("Email")):
                messagebox.showerror("Error", f"Email {fields.get('Email')} already exists.")
                return

            if fields.get("Password") and fields.get("Password") != fields.get("Confirm Password"):
                messagebox.showerror("Error", "Passwords do not match.")
                return

            all_fields = [field_name for field_name, value in fields.items() if value]

            if all_fields:
                backend_modules.add_new_user(
                    username=fields.get("Username"),
                    firstname=fields.get("First Name"),
                    lastname=fields.get("Last Name"),
                    email=fields.get("Email"),
                    password=fields.get("Password"),
                )
                messagebox.showinfo("Success", f"User {fields.get('Username')} added.")
                return

        if self.window is None:
            self.window = customtkinter.CTk()
            self.window.geometry("400x600+1000+100")
            self.window.resizable(0, 0)
            self.window.configure(bg_color="#7125FF")
            self.window.title("Add New User")

            heading_label = customtkinter.CTkLabel(
                self.window,
                text="EMS",
                font=("Goudy Old Style", 60, "bold"),
            )
            heading_label.place(x=145, y=10)

            new_username_entry = customtkinter.CTkEntry(
                self.window,
                width=300,
                placeholder_text="Username",
            )
            new_username_entry.place(x=53, y=130)

            new_firstname_entry = customtkinter.CTkEntry(
                self.window,
                width=300,
                placeholder_text="Firstname",
            )
            new_firstname_entry.place(x=53, y=180)

            new_lastname_entry = customtkinter.CTkEntry(
                self.window,
                width=300,
                placeholder_text="Lastname",
            )
            new_lastname_entry.place(x=53, y=230)

            new_email_entry = customtkinter.CTkEntry(
                self.window,
                width=300,
                placeholder_text="Email",
            )
            new_email_entry.place(x=53, y=280)

            new_password_entry = customtkinter.CTkEntry(
                self.window,
                width=300,
                placeholder_text="Password",
                show="*",
            )
            new_password_entry.place(x=53, y=330)

            confirm_password_entry = customtkinter.CTkEntry(
                self.window,
                width=300,
                placeholder_text="Confirm Password",
                show="*",
            )
            confirm_password_entry.place(x=53, y=380)

            add_user_button = customtkinter.CTkButton(
                self.window,
                text="Add user",
                cursor="hand2",
                hover_color="#1e0c0c",
                width=100,
                command=add_user
            )
            add_user_button.place(x=152, y=450)

            description = customtkinter.CTkTextbox(
                self.window,
                width=350,
                height=80,
            )
            text = """Password must contain at least six (6) characters with a mix of Upper and Lower case letters and at least one number."""
            description.place(x=30, y=500)
            description.insert("0.0", text)
            description.configure(state="disabled")

            self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.window.mainloop()


new_user_window = NewUserWindow()


def new_user() -> None:
    """Run new user window."""
    new_user_window.open_window()
