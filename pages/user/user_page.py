import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from uuid import UUID

from components.list_box_component import ListBoxComponent
from core.users_endpoints import user_api_client
from pages.base_page import BasePage


class UserPage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.user_data = []

    def _setup_ui(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        if self.controller:
            home_button = ttk.Button(self, text="< Back to Home",
                                     command=lambda: self.controller.show_page("HomePage"))
            home_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        else:
            print("Warning: Controller not provided to UserPage. 'Back to Home' button disabled.")

        title_label = tk.Label(self, text="Users", font=("Arial", 20, "bold"), pady=10)
        title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

        button_frame = tk.Frame(self, bg=self.cget('bg'))
        button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        user_trashbin_button = ttk.Button(button_frame, text="Users Trash Bin",
                                          command=lambda: self.controller.show_page("UserTrashBinPage"))
        user_trashbin_button.pack(side="left", padx=(0, 20))

        create_user_button = ttk.Button(button_frame, text="Create New User",
                                        command=lambda: self.controller.show_page("UserCreatePage"))
        create_user_button.pack(side="left")

        self.columns = ["id", "first_name", "last_name", "cpf", "email",
                        "manual_balance", "created_at", "updated_at", "deleted_at"]

        self.display_headings = {
            "id": "ID",
            "first_name": "First Name",
            "last_name": "Last Name",
            "cpf": "CPF",
            "email": "Email",
            "manual_balance": "Balance",
            "created_at": "Created At",
            "updated_at": "Updated At",
            "deleted_at": "Deleted At"
        }

        self.user_list_component = ListBoxComponent(self, columns=self.columns, display_headings=self.display_headings)
        self.user_list_component.grid(row=1, column=0, columnspan=2, padx=10, pady=10,
                                      sticky="nsew")
        self.user_list_component.on_select(self._on_user_selected)

        self._load_users()

    def _load_users(self):
        try:
            users_raw_data = user_api_client.get_all_users()
            self.user_data = users_raw_data
            items_for_list = []
            for user in users_raw_data:
                row_values = []
                for col in self.columns:
                    value = user.get(col, '')  # U
                    if isinstance(value, UUID):
                        row_values.append(str(value))
                    elif isinstance(value, datetime):
                        row_values.append(value.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        row_values.append(value)
                items_for_list.append(tuple(row_values))
            self.user_list_component.set_items(items_for_list)
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to load users: {e}")
            self.user_list_component.clear_list()

    def _on_user_selected(self, selected_values):
        if selected_values:
            user_id = selected_values[0]
            if self.controller:
                self.controller.show_page("UserUpdatePage", user_id=user_id)
            else:
                messagebox.showerror("Error", "Controller not available to show detail page.")
        else:
            pass

    def refresh(self):
        self._load_users()
