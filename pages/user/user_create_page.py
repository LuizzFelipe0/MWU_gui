from tkinter import messagebox, ttk

from ...components.detail_form_component import DetailFormComponent
from ...core.users_endpoints import user_api_client
from ...pages.base_page import BasePage


class UserCreatePage(BasePage):
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
            back_button = ttk.Button(self, text="< Back to Users",
                                     command=lambda: self.controller.show_page("UserPage"))
            back_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.user_fields_config = [
            {'label': 'First Name', 'key': 'first_name', 'type': 'entry'},
            {'label': 'Last Name', 'key': 'last_name', 'type': 'entry'},
            {'label': 'CPF', 'key': 'cpf', 'type': 'entry'},
            {'label': 'Email', 'key': 'email', 'type': 'entry'},
            {'label': 'Password', 'key': 'password', 'type': 'password'},  # Password field
            {'label': 'Manual Balance', 'key': 'manual_balance', 'type': 'entry'},
        ]

        self.detail_form = DetailFormComponent(
            self,
            fields_config=self.user_fields_config,
            on_save_callback=self._create_user,
            on_update_callback=None,
            on_delete_callback=None,
            on_cancel_callback=lambda: self.controller.show_page("UserPage"),
            title_text="Create New User",
            bg=self.cget('bg')
        )
        self.detail_form.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    def refresh(self, **kwargs):

        self.detail_form.set_data({})  # Ensure the form is empty
        if self.controller:
            self.controller.title("Create New User")

    def _create_user(self):
        user_data = self.detail_form.get_data()

        input_fields = ['first_name', 'last_name', 'cpf', 'email', 'password', 'manual_balance']
        payload = {k: v for k, v in user_data.items() if k in input_fields and v is not None}

        if 'manual_balance' in payload and payload['manual_balance']:
            try:
                payload['manual_balance'] = float(payload['manual_balance'])
            except ValueError:
                messagebox.showerror("Validation Error", "Manual Balance must be a number.")
                return

        if not payload.get('first_name') or not payload.get('email') or not payload.get('cpf') or not payload.get(
                'password'):
            messagebox.showerror("Validation Error", "First Name, CPF, Email, and Password are required.")
            return

        try:
            user_api_client.create_user(payload)
            messagebox.showinfo("Success", "User created successfully!")
            self.controller.show_page("UserPage")
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to create user: {e}")
