from tkinter import messagebox, ttk
from uuid import UUID

from components.detail_form_component import DetailFormComponent
from core.transactions_endpoints import transaction_api_client
from core.categories_endpoints import category_api_client
from core.users_endpoints import user_api_client
from pages.base_page import BasePage


class TransactionUpdatePage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.current_transaction_id = None
        self.users_cache = {}
        self.categories_cache = {}
        self.detail_form = None

    def _setup_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(3, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)

        if self.controller:
            back_button = ttk.Button(
                self,
                text="< Back to Transactions",
                command=lambda: self.controller.show_page("TransactionPage")
            )
            back_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.transaction_fields_config = [
            {'label': 'ID', 'key': 'id', 'type': 'entry', 'read_only': True},
            {'label': 'User', 'key': 'user_id', 'type': 'id_dropdown', 'options': {}},
            {'label': 'Category', 'key': 'category_id', 'type': 'id_dropdown', 'options': {}},
            {'label': 'Name', 'key': 'name', 'type': 'entry'},
            {'label': 'Description', 'key': 'description', 'type': 'entry'},
            {'label': 'Amount', 'key': 'amount', 'type': 'entry'},
            {'label': 'Date (YYYY-MM-DD)', 'key': 'date', 'type': 'entry'},
            {'label': 'Is Recurring', 'key': 'is_recurring', 'type': 'dropdown', 'options': ['True', 'False']},
            {'label': 'Recurrence Interval', 'key': 'recurrence_interval', 'type': 'dropdown',
             'options': ['Yearly', 'Monthly', 'Weekly', 'Daily']},
            {'label': 'Next Due Date (YYYY-MM-DD)', 'key': 'next_due_date', 'type': 'entry'},
        ]

    def refresh(self, transaction_id=None):
        if not transaction_id:
            messagebox.showwarning("Warning", "No category selected for update. Returning to list.")
            self._reset_form_and_navigate_back()
            return

        try:
            self.current_transaction_id = UUID(str(transaction_id))

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

            transaction_data = transaction_api_client.get_transaction_by_id(self.current_transaction_id)

            if self.detail_form:
                self.detail_form.destroy()

            self.detail_form = DetailFormComponent(
                self,
                fields_config=self.transaction_fields_config,
                on_save_callback=None,
                on_update_callback=self._update_transaction,
                on_delete_callback=self._delete_transaction,
                on_cancel_callback=lambda: self.controller.show_page("TransactionPage"),
                title_text="Update Transaction Details",
                bg=self.cget('bg')
            )
            self.detail_form.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
            self.detail_form.config(height=800)

            data_to_set = {
                'id': str(transaction_data.get('id', '')),
                'user_id': str(transaction_data.get('user_id', '')),
                'category_id': str(transaction_data.get('category_id', '')),
                'name': transaction_data.get('name', ''),
                'description': transaction_data.get('description', ''),
                'amount': transaction_data.get('amount', ''),
                'date': transaction_data.get('date', ''),
                'is_recurring': str(transaction_data.get('is_recurring', False)),
                'recurrence_interval': transaction_data.get('recurrence_interval', 'None')
                if transaction_data.get('recurrence_interval') is not None else 'None',
                'next_due_date': transaction_data.get('next_due_date', ''),
            }
            self.detail_form.set_data(data_to_set)

            if self.controller:
                self.controller.title(f"Update Transaction - {transaction_data.get('name', '')}")

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid ID format or data conversion error: {e}")
            self._reset_form_and_navigate_back()
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to load category details or users: {e}")
            self._reset_form_and_navigate_back()

    def _fetch_all_users_and_categories(self):
        try:
            users = user_api_client.get_all_users()
            self.users_cache = {str(user["id"]): user for user in users if user and "id" in user}

            categories = category_api_client.get_all_categories()
            self.categories_cache = {str(category["id"]): category for category in categories if
                                     category and "id" in category}
        except Exception as e:
            messagebox.showwarning("Data Load Warning", f"Could not load all users or Transaction Types: {e}")

    def _reset_form_and_navigate_back(self):
        self.detail_form.set_data({})
        self.current_transaction_id = None
        self.controller.show_page("TransactionPage")

    def _update_transaction(self):
        if not self.current_transaction_id:
            messagebox.showerror("Error", "No category selected for update.")
            return

        try:
            current_data = transaction_api_client.get_transaction_by_id(self.current_transaction_id)

            form_data = self.detail_form.get_data()

            modified_fields = {}

            updatable_fields = [
                'user_id', 'category_id', 'name', 'description', 'amount',
                'date', 'is_recurring', 'recurrence_interval', 'next_due_date'
            ]

            for field in updatable_fields:
                form_value = form_data.get(field)
                current_value = current_data.get(field)

                if field == 'is_recurring':
                    form_value_bool = (form_value == 'True')
                    if form_value_bool != current_value:
                        modified_fields[field] = form_value_bool
                    continue

                if field == 'recurrence_interval':
                    if form_value == 'None':
                        form_value = None
                    if form_value != current_value:
                        modified_fields[field] = form_value
                    continue

                if field == 'amount':
                    try:
                        form_value_float = float(form_value)
                        if form_value_float != current_value:
                            modified_fields[field] = form_value_float
                    except ValueError:
                        messagebox.showerror("Amount Error", "Amount value must be numeric.")
                        return
                    continue

                if field in ['user_id', 'category_id']:
                    if str(form_value) != str(current_value):
                        modified_fields[field] = str(form_value)
                    continue

                if str(form_value) != str(current_value):
                    modified_fields[field] = form_value

            if 'description' not in modified_fields and 'description' in form_data:
                modified_fields['description'] = form_data['description']

            if not modified_fields:
                messagebox.showinfo("Info", "There are no fields to update.")
                return

            response = transaction_api_client.update_transaction(self.current_transaction_id, modified_fields)

            if response:
                messagebox.showinfo("Success", "Transaction updated successfully!")
                self.controller.show_page("TransactionPage")
            else:
                messagebox.showerror("Error", "Received unexpected response from server")

        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid ID format: {e}")
        except Exception as e:
            messagebox.showerror(
                "API Error",
                f"Failed to update Transaction:\n{str(e)}\n"
                f"Please check if the server is running and accessible."
            )

    def _delete_transaction(self):
        if not self.current_transaction_id:
            messagebox.showerror("Error", "No Transaction selected for deletion.")
            return

        if messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete category ID {self.current_transaction_id}?"
        ):
            try:
                transaction_api_client.delete_transaction(self.current_transaction_id)
                messagebox.showinfo("Success", "Transaction deleted successfully (soft delete)!")
                self.controller.show_page("TransactionPage")
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to delete Transaction: {e}")