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

    def _setup_ui(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(3, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)
        if self.controller:
            back_button = ttk.Button(self, text="< Back to Categories",
                                     command=lambda: self.controller.show_page("TransactionPage"))
            back_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.category_fields_config = [
            {'label': 'ID', 'key': 'id', 'type': 'entry', 'read_only': True},
            {'label': 'User', 'key': 'user_id', 'type': 'id_dropdown', 'options': {}},
            {'label': 'Category', 'key': 'category_id', 'type': 'id_dropdown', 'options': {}},
            {'label': 'Name', 'key': 'name', 'type': 'entry'},
            {'label': 'Description', 'key': 'description', 'type': 'entry'},
            {'label': 'Amount', 'key': 'amount', 'type': 'entry'},
            {'label': 'Date', 'key': 'date', 'type': 'entry'},
            {'label': 'Is Recurring', 'key': 'is_recurring', 'type': 'entry'},
            {'label': 'Recurrence Interval', 'key': 'recurrence_interval','type': 'dropdown',
             'options': ['Yearly', 'Monthly','Weekly','Daily']},
            {'label': 'Next Due Date', 'key': 'next_due_date', 'type': 'entry'},
            {'label': 'Created At', 'key': 'created_at', 'type': 'entry', 'read_only': True},
            {'label': 'Updated At', 'key': 'updated_at', 'type': 'entry', 'read_only': True},
            {'label': 'Deleted At', 'key': 'deleted_at', 'type': 'entry', 'read_only': True}
        ]
        self.detail_form = DetailFormComponent(
            self,
            fields_config=self.category_fields_config,
            on_save_callback=None,
            on_update_callback=self._update_category,
            on_delete_callback=self._delete_category,
            on_cancel_callback=lambda: self.controller.show_page("TransactionPage"),
            title_text="Update Transaction Details",
            bg=self.cget('bg')
        )
        self.detail_form.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        self.detail_form.config(height=800)

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
                categories.get('name'): str(categories.get('id'))
                for categories in self.categories_cache.values()
                if categories and categories.get('id') and categories.get('name')
            }

            for field in self.category_fields_config:
                if field['key'] == 'user_id':
                    field['options'] = user_options
                if field['key'] == 'category_id':
                    field['options'] = category_options

            transaction_data = transaction_api_client.get_transaction_by_id(self.current_transaction_id)

            if self.detail_form:
                self.detail_form.destroy()

            self.detail_form = DetailFormComponent(
                self,
                fields_config=self.category_fields_config,
                on_save_callback=None,
                on_update_callback=self._update_category,
                on_delete_callback=self._delete_category,
                on_cancel_callback=lambda: self.controller.show_page("TransactionPage"),
                title_text="Update Transaction Details",
                bg=self.cget('bg')
            )
            self.detail_form.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

            data_to_set = {
                'id': str(transaction_data.get('id', '')),
                'user_id': str(transaction_data.get('user_id', '')),
                'category_id': str(transaction_data.get('category_id', '')),
                'name': transaction_data.get('name', ''),
                'description': transaction_data.get('description', ''),
                'amount': transaction_data.get('amount', ''),
                'date': transaction_data.get('date', ''),
                'is_recurring': transaction_data.get('is_recurring', ''),
                'recurrence_interval': transaction_data.get('recurrence_interval', ''),
                'next_due_date': transaction_data.get('next_due_date', ''),
                'created_at': transaction_data.get('created_at', ''),
                'updated_at': transaction_data.get('updated_at', ''),
                'deleted_at': transaction_data.get('deleted_at', '')
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
            self.categories_cache = {str(category["id"]): category for category in categories if category and "id" in category}
        except Exception as e:
            messagebox.showwarning("Data Load Warning", f"Could not load all users or Transaction Types: {e}")

    def _reset_form_and_navigate_back(self):
        self.detail_form.set_data({})
        self.current_transaction_id = None
        self.controller.show_page("TransactionPage")

    def _update_category(self):
        if not self.current_transaction_id:
            messagebox.showerror("Error", "No category selected for update.")
            return
        try:
            current_data = transaction_api_client.get_transaction_by_id(self.current_transaction_id)

            form_data = self.detail_form.get_data()

            modified_fields = {}
            for field in ['name', 'description', 'user_id', 'category_id']:
                current_value = str(current_data.get(field, ''))
                form_value = str(form_data.get(field, ''))

                if form_value and form_value != current_value:
                    modified_fields[field] = form_value

            if not modified_fields:
                messagebox.showinfo("Info", "No changes detected to update.")
                return

            payload = {}
            if 'name' in modified_fields:
                payload['name'] = modified_fields['name']
            if 'description' in modified_fields:
                payload['description'] = modified_fields['description']
            if 'user_id' in modified_fields:
                try:
                    payload['user_id'] = str(UUID(modified_fields['user_id']))
                except ValueError:
                    messagebox.showerror("Input Error", "Invalid User ID format")
                    return
            if 'category_id' in modified_fields:
                try:
                    payload['category_id'] = str(UUID(modified_fields['category_id']))
                except ValueError:
                    messagebox.showerror("Input Error", "Invalid Transaction Type ID format")
                    return

            response = transaction_api_client.update_transaction(self.current_transaction_id, payload)

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

    def _delete_category(self):
        if not self.current_transaction_id:
            messagebox.showerror("Error", "No Transaction selected for deletion.")
            return

        if messagebox.askyesno("Confirm Delete",
                               f"Are you sure you want to delete category ID {self.current_transaction_id}?"):
            try:
                transaction_api_client.delete_transaction(self.current_transaction_id)
                messagebox.showinfo("Success", "Transaction deleted successfully!")
                self.controller.show_page("TransactionPage")
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to delete Transaction: {e}")
