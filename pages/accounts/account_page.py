import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from uuid import UUID

from MWU_gui.components.list_box_component import ListBoxComponent
from MWU_gui.core.accounts_endpoints import account_api_client
from MWU_gui.pages.base_page import BasePage


class AccountsPage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.account_data = []

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
            print("Warning: Controller not provided to AccountPage. 'Back to Home' button disabled.")

        title_label = tk.Label(self, text="Accounts", font=("Arial", 20, "bold"), pady=10)
        title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

        create_account_button = ttk.Button(self, text="Create New Account",
                                        command=lambda: self.controller.show_page("AccountCreatePage"))
        create_account_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        self.columns = ["id", "name", "type", "account_number", "created_at", "updated_at",
                        "deleted_at"]

        self.display_headings = {
            "id": "ID",
            "name": "Name",
            "type": "Type",
            "account_number": "Account Number",
            "created_at": "Created At",
            "updated_at": "Updated At",
            "deleted_at": "Deleted At"
        }

        self.account_list_component = ListBoxComponent(self, columns=self.columns, display_headings=self.display_headings)
        self.account_list_component.grid(row=1, column=0, columnspan=2, padx=10, pady=10,
                                      sticky="nsew")
        self.account_list_component.on_select(self._on_account_selected)

        refresh_button = ttk.Button(self, text="Refresh Accounts", command=self._load_accounts)
        refresh_button.grid(row=2, column=0, columnspan=2, pady=5)

        self._load_accounts()

    def _load_accounts(self):
        try:
            accounts_raw_data = account_api_client.get_all_accounts()
            self.Account_data = accounts_raw_data
            items_for_list = []
            for account in accounts_raw_data:
                row_values = []
                for col in self.columns:
                    value = account.get(col, '')
                    if isinstance(value, UUID):
                        row_values.append(str(value))
                    elif isinstance(value, datetime):
                        row_values.append(value.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        row_values.append(value)
                items_for_list.append(tuple(row_values))
            self.account_list_component.set_items(items_for_list)
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to load Accounts: {e}")
            self.account_list_component.clear_list()

    def _on_account_selected(self, selected_values):
        if selected_values:
            account_id = selected_values[0]
            if self.controller:
                self.controller.show_page("AccountUpdatePage", account_id=account_id)  # Mudei para AccountUpdatePage
            else:
                messagebox.showerror("Error", "Controller not available to show detail page.")
        else:
            pass

    def refresh(self):
        self._load_accounts()
