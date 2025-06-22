from tkinter import messagebox, ttk
from uuid import UUID

from components.detail_form_component import DetailFormComponent
from core.financial_goals_endpoints import financial_goals_api_client
from core.users_endpoints import user_api_client
from pages.base_page import BasePage


class FinancialGoalsUpdatePage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.current_financial_goals_id = None
        self.users_cache = {}

    def _setup_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        if self.controller:
            back_button = ttk.Button(self, text="< Back to Financial Goals",
                                     command=lambda: self.controller.show_page("FinancialGoalsPage"))
            back_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.financial_goals_fields_config = [
            {'label': 'ID', 'key': 'id', 'type': 'entry', 'read_only': True},
            {'label': 'User', 'key': 'user_id', 'type': 'id_dropdown', 'options': {}},
            {'label': 'Name', 'key': 'name', 'type': 'entry'},
            {'label': 'Description', 'key': 'description', 'type': 'entry'},
            {'label': 'Target Amount', 'key': 'target_amount', 'type': 'entry'},
            {'label': 'Deadline', 'key': 'deadline', 'type': 'entry'},
            {'label': 'Created At', 'key': 'created_at', 'type': 'entry', 'read_only': True},
            {'label': 'Updated At', 'key': 'updated_at', 'type': 'entry', 'read_only': True}
        ]

        self.detail_form = None

    def refresh(self, financial_goals_id=None):
        if not financial_goals_id:
            messagebox.showwarning("Warning", "No financial goal selected for update. Returning to list.")
            self._reset_form_and_navigate_back()
            return

        try:
            self.current_financial_goals_id = UUID(str(financial_goals_id))

            self._fetch_all_users()
            user_options = {
                user.get('first_name'): str(user.get('id'))
                for user in self.users_cache.values()
                if user and user.get('id') and user.get('first_name')
            }

            for field in self.financial_goals_fields_config:
                if field['key'] == 'user_id':
                    field['options'] = user_options
                    break

            financial_goals_data = financial_goals_api_client.get_financial_goals_by_id(self.current_financial_goals_id)

            if self.detail_form:
                self.detail_form.destroy()

            self.detail_form = DetailFormComponent(
                self,
                fields_config=self.financial_goals_fields_config,
                on_save_callback=None,
                on_update_callback=self._update_financial_goals,
                on_delete_callback=self._delete_financial_goals,
                on_cancel_callback=lambda: self.controller.show_page("FinancialGoalsPage"),
                title_text="Update Financial Goal Details",
                bg=self.cget('bg')
            )
            self.detail_form.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

            data_to_set = {
                'id': str(financial_goals_data.get('id', '')),
                'user_id': str(financial_goals_data.get('user_id', '')),
                'name': financial_goals_data.get('name', ''),
                'description': financial_goals_data.get('description', ''),
                'target_amount': financial_goals_data.get('target_amount', ''),
                'deadline': financial_goals_data.get('deadline', ''),
                'created_at': financial_goals_data.get('created_at', ''),
                'updated_at': financial_goals_data.get('updated_at', '')
            }
            self.detail_form.set_data(data_to_set)

            if self.controller:
                self.controller.title(f"Update Financial Goal - {financial_goals_data.get('name', '')}")

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid ID format or data conversion error: {e}")
            self._reset_form_and_navigate_back()
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to load financial goal details or users: {e}")
            self._reset_form_and_navigate_back()

    def _fetch_all_users(self):
        try:
            users = user_api_client.get_all_users()
            self.users_cache = {str(user["id"]): user for user in users if user and "id" in user}
        except Exception as e:
            messagebox.showwarning("Data Load Warning", f"Failed to load all Users: {e}")

    def _reset_form_and_navigate_back(self):
        self.detail_form.set_data({})
        self.current_financial_goals_id = None
        self.controller.show_page("FinancialGoalsPage")

    def _update_financial_goals(self):
        if not self.current_financial_goals_id:
            messagebox.showerror("Error", "No financial goal selected for update.")
            return

        financial_goals_data = self.detail_form.get_data()

        update_fields = ['user_id', 'name', 'description', 'target_amount', 'deadline']
        payload = {k: v for k, v in financial_goals_data.items() if k in update_fields and v is not None}

        required_fields = ['user_id', 'name', 'target_amount', 'deadline']
        for field in required_fields:
            if not payload.get(field):
                messagebox.showerror("Validation Error", f"Please, fill all required fields. Missing: {field}")
                return
        try:
            payload['user_id'] = str(payload['user_id'])
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid User ID format: {e}")
            return

        try:
            payload['target_amount'] = float(payload['target_amount'])
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid Target Amount format: {e}")
            return

        try:
            financial_goals_api_client.update_financial_goals(self.current_financial_goals_id, payload)
            messagebox.showinfo("Success", "Financial Goal updated successfully!")
            self.controller.show_page("FinancialGoalsPage")
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to update Financial Goal: {e}")

    def _delete_financial_goals(self):
        if not self.current_financial_goals_id:
            messagebox.showerror("Error", "No Financial Goal selected for deletion.")
            return

        if messagebox.askyesno("Confirm Delete",
                               f"Are you sure you want to delete financial goal ID {self.current_financial_goals_id}?"):
            try:
                financial_goals_api_client.delete_financial_goals(self.current_financial_goals_id)
                messagebox.showinfo("Success", "Financial Goal deleted successfully!")
                self.controller.show_page("FinancialGoalsPage")
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to delete Financial Goal: {e}")