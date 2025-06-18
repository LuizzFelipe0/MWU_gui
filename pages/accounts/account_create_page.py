from tkinter import messagebox, ttk

from ...components.detail_form_component import DetailFormComponent
from ...core.accounts_endpoints import account_api_client
from ...pages.base_page import BasePage


class AccountCreatePage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)

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
            {'label': 'Name', 'key': 'name', 'type': 'entry'},
            {'label': 'Type', 'key': 'type', 'type': 'dropdown',
             'options': ['Investimentos', 'Poupança', 'Corrente', 'Salário']},
            {'label': 'Account Number', 'key': 'account_number', 'type': 'entry'},
            {'label': 'Balance', 'key': 'balance', 'type': 'entry'}
        ]

        self.detail_form = DetailFormComponent(
            self,
            fields_config=self.account_fields_config,
            on_save_callback=self._create_account,
            on_update_callback=None,
            on_delete_callback=None,
            on_cancel_callback=lambda: self.controller.show_page("AccountsPage"),
            title_text="Create New Account",
            bg=self.cget('bg')
        )
        self.detail_form.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    def refresh(self, **kwargs):
        self.detail_form.set_data({'name': '', 'type': '', 'account_number': '', 'balance': ''})
        if self.controller:
            self.controller.title("Create New Account")

    def _create_account(self):
        account_data = self.detail_form.get_data()

        input_fields = ['name', 'type', 'account_number', 'balance']

        payload = {k: v for k, v in account_data.items() if
                   k in input_fields and v is not None and v != ''}

        if payload.get('type') not in ['Investimentos', 'Poupança', 'Corrente']:
            messagebox.showerror("Validation Error", "Please select a valid account type.")
            return

        if 'balance' in payload and payload['balance']:
            try:
                payload['balance'] = float(payload['balance'])
            except ValueError:
                messagebox.showerror("Validation Error", "Balance must be a number.")
                return
        else:
            payload['balance'] = 0.0

        if not payload.get('name') or not payload.get('type') or not payload.get('account_number'):
            messagebox.showerror("Validation Error", "Name, Type, and Account Number are required.")
            return

        try:
            account_api_client.create_account(payload)
            messagebox.showinfo("Success", "Account created successfully!")
            self.controller.show_page("AccountsPage")
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to create account: {e}")
