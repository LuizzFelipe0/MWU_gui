import tkinter as tk
from tkinter import ttk, messagebox

from MWU_gui.components.list_box_component import ListBoxComponent
from MWU_gui.core.users_endpoints import users_api
from MWU_gui.pages.base_page import BasePage


class UserPage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.user_data = []

    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        if self.controller:
            home_button = ttk.Button(self, text="Back to Home",
                                     command=lambda: self.controller.show_page("HomePage"))
            home_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        else:
            print("Warning: Controller not provided to UserListPage. 'Back to Home' button disabled.")

        title_label = tk.Label(self, text="Users", font=("Arial", 20, "bold"), pady=10)
        title_label.grid(row=0, column=0, columnspan=2,
                         sticky="n")

        columns = ("id", "first_name", "last_name", "cpf", "email", "manual_balance")
        display_headings = {
            "id": "ID",
            "first_name": "First Name",
            "last_name": "Last Name",
            "cpf": "CPF",
            "email": "Email",
            "manual_balance": "Balance"
        }

        self.user_list_component = ListBoxComponent(self, columns=columns, display_headings=display_headings)
        self.user_list_component.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        refresh_button = ttk.Button(self, text="Refresh Users", command=self._load_users)
        refresh_button.grid(row=2, column=0, columnspan=2, pady=5)

        self.user_list_component.on_select(self._on_user_selected)

        self._load_users()

    def _load_users(self):
        try:
            users_raw_data = users_api.get_all_users()
            self.user_data = []
            items_for_list = []
            for user in users_raw_data:
                self.user_data.append(user)
                items_for_list.append((
                    user.get('id', ''),
                    user.get('first_name', ''),
                    user.get('last_name', ''),
                    user.get('cpf', ''),
                    user.get('email', ''),
                    user.get('manual_balance', '')
                ))
            self.user_list_component.set_items(items_for_list)
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to load users: {e}")
            self.user_list_component.clear_list()

    def _on_user_selected(self, selected_values):
        if selected_values:
            user_id = selected_values[0]
            print(f"User selected: ID={user_id}, Name={selected_values[1]}")
            messagebox.showinfo("User Selected", f"You selected User ID: {user_id}")

    def refresh(self):
        self._load_users()
