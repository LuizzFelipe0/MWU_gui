from tkinter import messagebox, ttk
from uuid import UUID

from components.detail_form_component import DetailFormComponent
from core.user_accounts_endpoints import users_accounts_api_client
from core.users_endpoints import user_api_client
from core.accounts_endpoints import account_api_client
from pages.base_page import BasePage


class UserAccountsUpdatePage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.current_user_account_id = None
        self.users_cache = {}
        self.accounts_cache = {}
        self.detail_form = None
        self._setup_ui()

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

        self.user_accounts_fields_config = [
            {'label': 'User Account ID', 'key': 'id', 'type': 'entry', 'read_only': True},
            {'label': 'User Name', 'key': 'user_name', 'type': 'entry', 'read_only': True},
            {'label': 'Account Name', 'key': 'account_name', 'type': 'entry', 'read_only': True},
            {'label': 'User ID (Hidden)', 'key': 'user_id', 'type': 'entry', 'read_only': True, 'show': False},
            {'label': 'Account ID (Hidden)', 'key': 'account_id', 'type': 'entry', 'read_only': True, 'show': False},
            {'label': 'Created At', 'key': 'created_at', 'type': 'entry', 'read_only': True}
        ]

        self.detail_form = DetailFormComponent(
            self,
            fields_config=self.user_accounts_fields_config,
            on_save_callback=None,
            on_update_callback=None,
            on_delete_callback=self._delete_user_account_relationship,
            on_cancel_callback=lambda: self.controller.show_page("UserAccountsPage"),
            title_text="Delete User Account Relationship",
            bg=self.cget('bg')
        )
        self.detail_form.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    def refresh(self, user_account_id=None):
        self._fetch_all_users_and_accounts()

        if user_account_id:
            try:
                self.current_user_account_id = UUID(str(user_account_id))
                user_account_data = users_accounts_api_client.get_users_accounts_by_id(self.current_user_account_id)

                if user_account_data is None:
                    messagebox.showerror("Error", f"User Account with ID {user_account_id} not found.")
                    self._reset_form_and_navigate_back()
                    return

                user_id = user_account_data.get('user_id')
                account_id = user_account_data.get('account_id')

                user_name = self.users_cache.get(str(user_id), {}).get('first_name', 'Unknown User')
                account_name = self.accounts_cache.get(str(account_id), {}).get('name', 'Unknown Account')

                created_at_val = user_account_data.get('created_at', '')
                if isinstance(created_at_val, str) and 'T' in created_at_val:
                    created_at_val = created_at_val.split('T')[0]  # Only date part

                display_data = {
                    'id': str(user_account_data.get('id', '')),
                    'user_name': user_name,
                    'account_name': account_name,
                    'user_id': str(user_id) if user_id else '',
                    'account_id': str(account_id) if account_id else '',
                    'created_at': created_at_val
                }

                self.detail_form.set_data(display_data)

                if self.controller:
                    self.controller.title(f"Delete User Account - {user_name} - {account_name}")
            except ValueError:
                messagebox.showerror("Error", f"Invalid User Account ID format: {user_account_id}")
                self._reset_form_and_navigate_back()
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to load user account details: {e}")
                self._reset_form_and_navigate_back()
        else:
            messagebox.showwarning("Warning", "No user account selected for deletion. Returning to list.")
            self._reset_form_and_navigate_back()

    def _fetch_all_users_and_accounts(self):
        try:
            users = user_api_client.get_all_users()
            self.users_cache = {str(user["id"]): user for user in users if user and "id" in user}

            accounts = account_api_client.get_all_accounts()
            self.accounts_cache = {str(account["id"]): account for account in accounts if account and "id" in account}
        except Exception as e:
            messagebox.showwarning("Data Load Warning", f"Could not load all users or accounts for display: {e}")

    def _reset_form_and_navigate_back(self):
        if self.detail_form:  
            self.detail_form.set_data({})
        self.current_user_account_id = None
        self.controller.show_page("UserAccountsPage")

    def _delete_user_account_relationship(self):
        if not self.current_user_account_id:
            messagebox.showerror("Error", "No User Account relationship selected for deletion.")
            return

        try:
            current_data = users_accounts_api_client.get_users_accounts_by_id(self.current_user_account_id)
            user_id = current_data.get('user_id')
            account_id = current_data.get('account_id')
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to retrieve User ID and Account ID for deletion: {e}")
            return  

        if not user_id or not account_id:
            messagebox.showerror("Error", "Could not retrieve User ID or Account ID for deletion.")
            return

        if messagebox.askyesno("Confirm Delete",
                               f"Are you sure you want to delete the relationship between User '{self.users_cache.get(str(user_id), {}).get('first_name', 'Unknown')}' "
                               f"and Account '{self.accounts_cache.get(str(account_id), {}).get('name', 'Unknown')}'?"):
            try:
                users_accounts_api_client.delete_users_accounts(UUID(str(user_id)), UUID(str(account_id)))
                messagebox.showinfo("Success", "User Account relationship deleted successfully!")
                self.controller.show_page("UserAccountsPage")
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to delete User Account relationship: {e}")