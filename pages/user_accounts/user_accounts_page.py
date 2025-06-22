import tkinter as tk
from tkinter import ttk, messagebox

from components.list_box_component import ListBoxComponent
from core.user_accounts_endpoints import users_accounts_api_client
from core.users_endpoints import user_api_client
from core.accounts_endpoints import account_api_client
from pages.base_page import BasePage


class UserAccountsPage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.user_accounts_data = []
        self.users_cache = {}
        self.accounts_cache = {}

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
            pass

        title_label = tk.Label(self, text="User Accounts", font=("Arial", 20, "bold"), pady=10)
        title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

        create_user_accounts_button = ttk.Button(self, text="Create New User Account",
                                                 command=lambda: self.controller.show_page("UserAccountsCreatePage"))
        create_user_accounts_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        self.columns = ["id", "user_name", "account_name", "created_at"]

        self.display_headings = {
            "id": "ID",
            "user_name": "User Name",
            "account_name": "Account Name",
            "created_at": "Created At"
        }

        self.user_accounts_list_component = ListBoxComponent(self, columns=self.columns,
                                                             display_headings=self.display_headings)
        self.user_accounts_list_component.grid(row=1, column=0, columnspan=2, padx=10, pady=10,
                                               sticky="nsew")
        self.user_accounts_list_component.on_select(self._on_user_accounts_selected)

        self._load_user_accounts()

    def _load_user_accounts(self):
        try:
            self._fetch_all_users_and_accounts()
            user_accounts_raw_data = users_accounts_api_client.get_all_users_accounts()
            self.user_accounts_data = user_accounts_raw_data

            items_for_list = []
            for user_account in user_accounts_raw_data:
                user_id = user_account.get("user_id")
                account_id = user_account.get("account_id")

                user_name = self.users_cache.get(str(user_id), {}).get("first_name", "Unknown User")
                account_name = self.accounts_cache.get(str(account_id), {}).get("name", "Unknown Account")

                row_values = [
                    str(user_account.get("id", '')),
                    user_name,
                    account_name,
                    user_account.get("created_at", '').split('T')[0] if isinstance(user_account.get("created_at"),
                                                                                   str) else ''
                ]
                items_for_list.append(tuple(row_values))
            self.user_accounts_list_component.set_items(items_for_list)
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to load User Accounts: {e}")
            self.user_accounts_list_component.clear_list()

    def _fetch_all_users_and_accounts(self):
        try:
            users = user_api_client.get_all_users()
            self.users_cache = {str(user["id"]): user for user in users if user and "id" in user}

            accounts = account_api_client.get_all_accounts()
            self.accounts_cache = {str(account["id"]): account for account in accounts if account and "id" in account}
        except Exception as e:
            messagebox.showwarning("Data Load Warning", f"Could not load all users or accounts: {e}")

    def _on_user_accounts_selected(self, selected_values):
        if selected_values:
            user_accounts_id = selected_values[0]
            if self.controller:
                self.controller.show_page("UserAccountsUpdatePage", user_account_id=user_accounts_id)
            else:
                pass
        else:
            pass

    def refresh(self):
        self._load_user_accounts()