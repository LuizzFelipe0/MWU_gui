from tkinter import messagebox, ttk

from components.detail_form_component import DetailFormComponent
from core.financial_goals_endpoints import financial_goals_api_client
from core.users_endpoints import user_api_client
from pages.base_page import BasePage


class FinancialGoalsCreatePage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.users_cache = {}
        self.detail_form = None

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

        self.financial_goal_fields_config = [
            {'label': 'User', 'key': 'user_id', 'type': 'id_dropdown', 'options': {}},
            {'label': 'Name', 'key': 'name', 'type': 'entry'},
            {'label': 'Description', 'key': 'description', 'type': 'entry'},
            {'label': 'Target Amount', 'key': 'target_amount', 'type': 'entry'},
            {'label': 'Deadline', 'key': 'deadline', 'type': 'entry'}
        ]

    def refresh(self, **kwargs):
        self._fetch_all_users()

        user_options = {
            user.get('first_name'): str(user.get('id'))
            for user in self.users_cache.values()
            if user and user.get('id') and user.get('first_name')
        }

        for field in self.financial_goal_fields_config:
            if field['key'] == 'user_id':
                field['options'] = user_options
                break

        if self.detail_form:
            self.detail_form.destroy()

        self.detail_form = DetailFormComponent(
            self,
            fields_config=self.financial_goal_fields_config,
            on_save_callback=self._create_financial_goal,
            on_update_callback=None,
            on_delete_callback=None,
            on_cancel_callback=lambda: self.controller.show_page("FinancialGoalsPage"),
            title_text="Create New Financial Goals",
            bg=self.cget('bg')
        )
        self.detail_form.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        self.detail_form.set_data({
            'user_id': '',
            'name': '',
            'description': '',
            'target_amount': '',
            'deadline': ''
        })

        if self.controller:
            self.controller.title("Create New Financial Goal")

    def _fetch_all_users(self):
        try:
            users = user_api_client.get_all_users()
            self.users_cache = {str(user["id"]): user for user in users if user and "id" in user}
        except Exception as e:
            messagebox.showwarning("Data Load Warning", f"Not possible to load all users: {e}")

    def _create_financial_goal(self):
        financial_goal_data = self.detail_form.get_data()

        required_fields = ['user_id', 'name', 'target_amount', 'deadline']
        for field in required_fields:
            if not financial_goal_data.get(field):
                messagebox.showerror("Validation Error", f"Please, fill all fields. Missing: {field}")
                return

        try:
            payload = {
                'user_id': str(financial_goal_data['user_id']),
                'name': financial_goal_data['name'],
                'description': financial_goal_data.get('description', ''),
                'target_amount': float(financial_goal_data['target_amount']),
                'deadline': financial_goal_data['deadline']
            }

            response = financial_goals_api_client.create_financial_goals(payload)

            if response and isinstance(response, dict) and response.get('id'):
                messagebox.showinfo("Sucesso", "Sucessfully created Financial Goal!")
                self.controller.show_page("FinancialGoalsPage")
            elif response and isinstance(response, dict) and response.get('message'):
                messagebox.showerror("Erro de API", response.get('message'))
            else:
                error_message = f"Unknown Error. Response format da API inesperado: {response}"
                messagebox.showerror("Erro de API", error_message)

        except ValueError as ve:
            messagebox.showerror("Erro de Entrada", f"Please, verify entry formats. Error: {ve}")
        except Exception as e:
            messagebox.showerror("Erro de API", f"Failed to create financial goal: {e}")