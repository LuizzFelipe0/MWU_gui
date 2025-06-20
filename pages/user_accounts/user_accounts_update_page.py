from tkinter import messagebox, ttk
from uuid import UUID

from ...components.detail_form_component import DetailFormComponent
from ...core.user_accounts_endpoints import users_accounts_api_client
from ...pages.base_page import BasePage


class UserAccountsUpdatePage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.current_users_accounts_id = None

    def _setup_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        if self.controller:
            back_button = ttk.Button(self, text="< Back to Accounts",
                                     command=lambda: self.controller.show_page("UserAccountsPage"))
            back_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.users_accounts_fields_config = [
            {'label': 'ID', 'key': 'id', 'type': 'entry', 'read_only': True},
            {'label': 'user_id', 'key': 'user_id', 'type': 'entry'},
            {'label': 'users_accounts_id', 'key': 'users_accounts_id', 'type': 'entry'},
            {'label': 'Created At', 'key': 'created_at', 'type': 'entry', 'read_only': True}
        ]

        self.detail_form = DetailFormComponent(
            self,
            fields_config=self.users_accounts_fields_config,
            on_save_callback=None,
            on_update_callback=self._update_users_accounts,
            on_delete_callback=self._delete_users_accounts,
            on_cancel_callback=lambda: self.controller.show_page("UserAccountsPage"),
            title_text="Update Account Details",
            bg=self.cget('bg')
        )
        self.detail_form.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    def refresh(self, users_accounts_id=None):

        if users_accounts_id:
            try:
                self.current_users_accounts_id = UUID(str(users_accounts_id))
                users_accounts_data = users_accounts_api_client.get_users_accounts_by_id(self.current_users_accounts_id)
                self.detail_form.set_data(users_accounts_data)
                if self.controller:
                    self.controller.title(f"Update Account - {users_accounts_data.get('name', '')}")
            except ValueError:
                messagebox.showerror("Error", f"Invalid Account ID format: {users_accounts_id}")
                self._reset_form_and_navigate_back()
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to load users_accounts details: {e}")
                self._reset_form_and_navigate_back()
        else:
            messagebox.showwarning("Warning", "No users_accounts selected for update. Returning to list.")
            self._reset_form_and_navigate_back()

    def _reset_form_and_navigate_back(self):
        self.detail_form.set_data({})
        self.current_users_accounts_id = None
        self.controller.show_page("UserAccountsPage")

    def _update_users_accounts(self):
        if not self.current_users_accounts_id:
            messagebox.showerror("Error", "No users_accounts selected for update.")
            return

        users_accounts_data = self.detail_form.get_data()

        update_fields = ['name', 'type', 'users_accounts_number', 'balance']
        payload = {k: v for k, v in users_accounts_data.items() if k in update_fields and v is not None}

        if 'balance' in payload and payload['balance']:
            try:
                payload['balance'] = float(payload['balance'])
            except ValueError:
                messagebox.showerror("Validation Error", "Manual Balance must be a number.")
                return
        try:
            users_accounts_api_client.update_users_accounts(self.current_users_accounts_id, payload)
            messagebox.showinfo("Success", "Account updated successfully!")
            self.controller.show_page("UserAccountsPage")
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to update users_accounts: {e}")

    def _delete_users_accounts(self):
        if not self.current_users_accounts_id:
            messagebox.showerror("Error", "No users_accounts selected for deletion.")
            return

        if messagebox.askyesno("Confirm Delete",
                               f"Are you sure you want to delete users_accounts ID {self.current_users_accounts_id}?"):
            try:
                users_accounts_api_client.delete_users_accounts(self.current_users_accounts_id)
                messagebox.showinfo("Success", "Account deleted successfully (soft delete)!")
                self.controller.show_page("UserAccountsPage")
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to delete users_accounts: {e}")
