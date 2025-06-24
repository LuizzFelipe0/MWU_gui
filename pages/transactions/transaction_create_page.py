from tkinter import messagebox, ttk
from uuid import UUID

from components.detail_form_component import DetailFormComponent
from core.transactions_endpoints import transaction_api_client
from core.categories_endpoints import category_api_client
from core.users_endpoints import user_api_client
from pages.base_page import BasePage


class TransactionCreatePage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.users_cache = {}
        self.categories_cache = {}
        self.detail_form = None
        self._setup_ui()

    def _setup_ui(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        if self.controller:
            back_button = ttk.Button(self, text="< Back to Transactions",
                                     command=lambda: self.controller.show_page("TransactionPage"))
            back_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.transaction_fields_config = [
            {'label': 'User', 'key': 'user_id', 'type': 'id_dropdown', 'options': {}},
            {'label': 'Category', 'key': 'category_id', 'type': 'id_dropdown', 'options': {}},
            {'label': 'Name', 'key': 'name', 'type': 'entry'},
            {'label': 'Description', 'key': 'description', 'type': 'entry'},
            {'label': 'Amount', 'key': 'amount', 'type': 'entry'},
            {'label': 'Date (YYYY-MM-DD)', 'key': 'date', 'type': 'entry'},
            {'label': 'Is Recurring', 'key': 'is_recurring', 'type': 'dropdown', 'options': ['True', 'False']},
            {'label': 'Recurrence Interval', 'key': 'recurrence_interval', 'type': 'dropdown',
             'options': ['Yearly', 'Monthly', 'Weekly', 'Daily', 'None']},
            {'label': 'Next Due Date (YYYY-MM-DD)', 'key': 'next_due_date', 'type': 'entry'},
        ]

    def refresh(self, **kwargs):
        self._fetch_all_users_and_categories()

        user_options = {
            user.get('first_name'): str(user.get('id'))
            for user in self.users_cache.values()
            if user and user.get('id') and user.get('first_name')
        }

        category_options = {
            category.get('name'): str(category.get('id'))
            for category in self.categories_cache.values()
            if category and category.get('id') and category.get('name')
        }

        for field in self.transaction_fields_config:
            if field['key'] == 'user_id':
                field['options'] = user_options
            elif field['key'] == 'category_id':
                field['options'] = category_options
            elif field['key'] == 'is_recurring':
                field['options'] = ['True', 'False']
            elif field['key'] == 'recurrence_interval':
                field['options'] = ['Yearly', 'Monthly', 'Weekly', 'Daily', 'None']

        if self.detail_form:
            self.detail_form.destroy()

        self.detail_form = DetailFormComponent(
            self,
            fields_config=self.transaction_fields_config,
            on_save_callback=self._create_transaction,
            on_update_callback=None,
            on_delete_callback=None,
            on_cancel_callback=lambda: self.controller.show_page("TransactionPage"),
            title_text="Create New Transaction",
            bg=self.cget('bg')
        )
        self.detail_form.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        self.detail_form.set_data({
            'user_id': '',
            'category_id': '',
            'name': '',
            'description': '',
            'amount': '',
            'date': '',
            'is_recurring': 'False',
            'recurrence_interval': 'None',
            'next_due_date': '',
        })

        if self.controller:
            self.controller.title("Create New Transaction")

    def _fetch_all_users_and_categories(self):
        try:
            users = user_api_client.get_all_users()
            self.users_cache = {str(user["id"]): user for user in users if user and "id" in user}

            categories = category_api_client.get_all_categories()
            self.categories_cache = {
                str(category["id"]): category
                for category in categories
                if category and "id" in category
            }
        except Exception as e:
            messagebox.showwarning("Data Load Warning", f"Could not load all users or categories: {e}")

    def _create_transaction(self):
        transaction_data = self.detail_form.get_data()

        required_fields = ['user_id', 'category_id', 'name', 'amount', 'date', 'is_recurring']
        for field in required_fields:
            if not transaction_data.get(field):
                messagebox.showerror("Validation Error", f"Please fill all required fields. Missing: {field}")
                return

        try:
            payload = {
                'user_id': str(UUID(transaction_data['user_id'])),
                'category_id': str(UUID(transaction_data['category_id'])),
                'name': transaction_data['name'],
                'description': transaction_data.get('description', ''),
                'amount': float(transaction_data['amount']),
                'date': transaction_data['date'],
                'is_recurring': (transaction_data['is_recurring'] == 'True'),
            }

            response = transaction_api_client.create_transaction(payload)

            if response and isinstance(response, dict) and response.get('id'):
                messagebox.showinfo("Success", "Transaction created successfully!")
                self.controller.show_page("TransactionPage")
            elif response and isinstance(response, dict) and response.get('message'):
                messagebox.showerror("API Error", response.get('message'))
            else:
                error_message = f"Unknown Error. Unexpected API response format: {response}"
                messagebox.showerror("API Error", error_message)

        except ValueError as ve:
            messagebox.showerror("Input Error", f"Please verify input formats (e.g., Amount, Dates). Error: {ve}")
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to create transaction: {e}")