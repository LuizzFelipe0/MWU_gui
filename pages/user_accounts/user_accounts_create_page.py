from tkinter import messagebox, ttk
from uuid import UUID

from components.detail_form_component import DetailFormComponent
from core.accounts_endpoints import account_api_client
from core.users_endpoints import user_api_client
from core.user_accounts_endpoints import users_accounts_api_client
from pages.base_page import BasePage


class UserAccountsCreatePage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.users_cache = {}
        self.accounts_cache = {}
        self.detail_form = None

    def _setup_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        if self.controller:
            back_button = ttk.Button(self, text="< Back to User Accounts",
                                     command=lambda: self.controller.show_page("UserAccountsPage"))
            back_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.user_account_fields_config = [
            {'label': 'User', 'key': 'user_id', 'type': 'id_dropdown', 'options': {}},
            {'label': 'Account', 'key': 'account_id', 'type': 'id_dropdown', 'options': {}}
        ]

    def refresh(self, **kwargs):
        self._fetch_all_users_and_accounts()

        user_options = {user.get('first_name'): str(user.get('id')) for user in self.users_cache.values() if user and user.get('id') and user.get('first_name')}
        account_options = {account.get('name'): str(account.get('id')) for account in self.accounts_cache.values() if account and account.get('id') and account.get('name')}

        for field in self.user_account_fields_config:
            if field['key'] == 'user_id':
                field['options'] = user_options
            elif field['key'] == 'account_id':
                field['options'] = account_options

        if self.detail_form:
            self.detail_form.destroy()

        self.detail_form = DetailFormComponent(
            self,
            fields_config=self.user_account_fields_config,
            on_save_callback=self._create_user_account,
            on_update_callback=None,
            on_delete_callback=None,
            on_cancel_callback=lambda: self.controller.show_page("UserAccountsPage"),
            title_text="Create New User Account Relationship",
            bg=self.cget('bg')
        )
        self.detail_form.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        self.detail_form.set_data({'user_id': '', 'account_id': ''})
        if self.controller:
            self.controller.title("Create New User Account Relationship")

    def _fetch_all_users_and_accounts(self):
        try:
            users = user_api_client.get_all_users()
            self.users_cache = {str(user["id"]): user for user in users if user and "id" in user}

            accounts = account_api_client.get_all_accounts()
            self.accounts_cache = {str(account["id"]): account for account in accounts if account and "id" in account}
        except Exception as e:
            messagebox.showwarning("Data Load Warning", f"Could not load all users or accounts for dropdowns: {e}")

    def _create_user_account(self):
        try:
            user_account_data = self.detail_form.get_data()

            if not all(user_account_data.values()):
                missing = [k for k, v in user_account_data.items() if not v]
                messagebox.showerror(
                    "Validation Error",
                    f"Please select values for: {', '.join(missing)}"
                )
                return

            user_id_val = user_account_data['user_id']
            account_id_val = user_account_data['account_id']

            user_uuid = UUID(user_id_val)
            account_uuid = UUID(account_id_val)

            response = users_accounts_api_client.create_user_accounts(
                user_id=user_uuid,
                account_id=account_uuid
            )

            if response and isinstance(response, dict) and response.get('id'):
                messagebox.showinfo("Success", "Relationship created successfully!")
                self.controller.show_page("UserAccountsPage")
            elif response and isinstance(response, dict) and response.get('message'):
                messagebox.showerror("API Error", response.get('message'))
            else:
                error_message = f"Unknown error occurred. Unexpected API response format: {response}"
                messagebox.showerror("API Error", error_message)

        except Exception as e:
            messagebox.showerror(
                "Operation Failed",
                f"Could not create relationship:\n{str(e)}"
            )