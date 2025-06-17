from tkinter import messagebox, ttk
from uuid import UUID

from ...components.detail_form_component import DetailFormComponent
from ...core.accounts_endpoints import account_api_client
from ...pages.base_page import BasePage


class AccountUpdatePage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.current_account_id = None

    def _setup_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        if self.controller:
            back_button = ttk.Button(self, text="< Back to Accounts",
                                     command=lambda: self.controller.show_page("AccountsPage"))
            back_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.account_fields_config = [
            {'label': 'ID', 'key': 'id', 'type': 'entry', 'read_only': True},
            {'label': 'Name', 'key': 'name', 'type': 'entry'},
            {'label': 'Type', 'key': 'type', 'type': 'entry'},
            {'label': 'Account Number', 'key': 'account_number', 'type': 'entry'},
            {'label': 'Balance', 'key': 'balance', 'type': 'entry'},
            {'label': 'Created At', 'key': 'created_at', 'type': 'entry', 'read_only': True},
            {'label': 'Updated At', 'key': 'updated_at', 'type': 'entry', 'read_only': True},
            {'label': 'Deleted At', 'key': 'deleted_at', 'type': 'entry', 'read_only': True},
        ]

        self.detail_form = DetailFormComponent(
            self,
            fields_config=self.account_fields_config,
            on_save_callback=None,
            on_update_callback=self._update_account,
            on_delete_callback=self._delete_account,
            on_cancel_callback=lambda: self.controller.show_page("AccountsPage"),
            title_text="Update Account Details",
            bg=self.cget('bg')
        )
        self.detail_form.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    def refresh(self, account_id=None):

        if account_id:
            try:
                self.current_account_id = UUID(str(account_id))
                account_data = account_api_client.get_account_by_id(self.current_account_id)
                self.detail_form.set_data(account_data)
                if self.controller:
                    self.controller.title(f"Update Account - {account_data.get('name', '')}")
            except ValueError:
                messagebox.showerror("Error", f"Invalid Account ID format: {account_id}")
                self._reset_form_and_navigate_back()
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to load account details: {e}")
                self._reset_form_and_navigate_back()
        else:
            messagebox.showwarning("Warning", "No account selected for update. Returning to list.")
            self._reset_form_and_navigate_back()

    def _reset_form_and_navigate_back(self):
        self.detail_form.set_data({})
        self.current_account_id = None
        self.controller.show_page("AccountsPage")

    def _update_account(self):
        if not self.current_account_id:
            messagebox.showerror("Error", "No account selected for update.")
            return

        account_data = self.detail_form.get_data()

        update_fields = ['name', 'type', 'account_number', 'balance']
        payload = {k: v for k, v in account_data.items() if k in update_fields and v is not None}

        if 'balance' in payload and payload['balance']:
            try:
                payload['balance'] = float(payload['balance'])
            except ValueError:
                messagebox.showerror("Validation Error", "Manual Balance must be a number.")
                return
        try:
            account_api_client.update_account(self.current_account_id, payload)
            messagebox.showinfo("Success", "Account updated successfully!")
            self.controller.show_page("AccountsPage")
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to update account: {e}")

    def _delete_account(self):
        if not self.current_account_id:
            messagebox.showerror("Error", "No account selected for deletion.")
            return

        if messagebox.askyesno("Confirm Delete",
                               f"Are you sure you want to delete account ID {self.current_account_id}?"):
            try:
                account_api_client.delete_account(self.current_account_id)
                messagebox.showinfo("Success", "Account deleted successfully (soft delete)!")
                self.controller.show_page("AccountsPage")
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to delete account: {e}")
