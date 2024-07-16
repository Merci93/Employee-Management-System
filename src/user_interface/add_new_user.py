"""Module to create a new user."""
import customtkinter


class NewUserWindow:
    def __init__(self):
        self.window = None

    def on_closing(self):
        self.window.destroy()
        self.window = None

    def open_window(self):
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
            heading_label.place(x=145, y=30)

            new_username_entry = customtkinter.CTkEntry(
                self.window,
                width=300,
                placeholder_text="Username",
            )
            new_username_entry.place(x=53, y=150)

            new_firstname_entry = customtkinter.CTkEntry(
                self.window,
                width=300,
                placeholder_text="Firstname",
            )
            new_firstname_entry.place(x=53, y=200)

            new_lastname_entry = customtkinter.CTkEntry(
                self.window,
                width=300,
                placeholder_text="Lastname",
            )
            new_lastname_entry.place(x=53, y=250)

            new_password_entry = customtkinter.CTkEntry(
                self.window,
                width=300,
                placeholder_text="Password",
                show="*",
            )
            new_password_entry.place(x=53, y=300)

            confirm_password_entry = customtkinter.CTkEntry(
                self.window,
                width=300,
                placeholder_text="Confirm Password",
                show="*",
            )
            confirm_password_entry.place(x=53, y=350)

            add_user_button = customtkinter.CTkButton(
                self.window,
                text="Add user",
                cursor="hand2",
                hover_color="#1e0c0c",
                width=100,
            )
            add_user_button.place(x=152, y=430)

            description = customtkinter.CTkTextbox(
                self.window,
                width=350,
                height=80,
            )
            text = """Password must contain at least six (6) characters with a mix of Upper and Lower case letters and at least one number."""
            description.place(x=30, y=480)
            description.insert("0.0", text)
            description.configure(state="disabled")

            self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
            self.window.mainloop()


new_user_window = NewUserWindow()


def new_user() -> None:
    """Run new user window."""
    new_user_window.open_window()


new_user()
