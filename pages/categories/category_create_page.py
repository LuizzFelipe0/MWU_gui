from tkinter import messagebox, ttk

from components.detail_form_component import DetailFormComponent
from core.categories_endpoints import category_api_client
from core.category_types_endpoints import category_type_api_client
from core.users_endpoints import user_api_client
from pages.base_page import BasePage


class CategoryCreatePage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.users_cache = {}
        self.category_types_cache = {}
        self.detail_form = None

    def _setup_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        if self.controller:
            back_button = ttk.Button(self, text="< Back to Categories",
                                   command=lambda: self.controller.show_page("CategoryPage"))
            back_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.category_fields_config = [
            {'label': 'User', 'key': 'user_id', 'type': 'id_dropdown', 'options': {}},
            {'label': 'Category Type', 'key': 'category_type_id', 'type': 'id_dropdown', 'options': {}},
            {'label': 'Name', 'key': 'name', 'type': 'entry'},
            {'label': 'Description', 'key': 'description', 'type': 'entry'}
        ]

    def refresh(self, **kwargs):
        self._fetch_all_users_and_category_types()

        user_options = {
            user.get('first_name'): str(user.get('id'))
            for user in self.users_cache.values()
            if user and user.get('id') and user.get('first_name')
        }

        category_types_options = {
            category_type.get('name'): str(category_type.get('id'))
            for category_type in self.category_types_cache.values()
            if category_type and category_type.get('id') and category_type.get('name')
        }

        for field in self.category_fields_config:
            if field['key'] == 'user_id':
                field['options'] = user_options
            if field['key'] == 'category_type_id':
                field['options'] = category_types_options

        if self.detail_form:
            self.detail_form.destroy()

        self.detail_form = DetailFormComponent(
            self,
            fields_config=self.category_fields_config,
            on_save_callback=self._create_category,
            on_update_callback=None,
            on_delete_callback=None,
            on_cancel_callback=lambda: self.controller.show_page("CategoryPage"),
            title_text="Create New Category",
            bg=self.cget('bg')
        )
        self.detail_form.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        self.detail_form.set_data({
            'user_id': '',
            'category_type_id': '',
            'name': '',
            'description': ''
        })

        if self.controller:
            self.controller.title("Create New Category")

    def _fetch_all_users_and_category_types(self):
        try:
            users = user_api_client.get_all_users()
            self.users_cache = {str(user["id"]): user for user in users if user and "id" in user}

            category_types = category_type_api_client.get_all_category_types()
            self.category_types_cache = {
                str(category_type["id"]): category_type
                for category_type in category_types
                if category_type and "id" in category_type
            }
        except Exception as e:
            messagebox.showwarning("Data Load Warning", f"Could not load all users or Category Types: {e}")

    def _create_category(self):
        category_data = self.detail_form.get_data()

        required_fields = ['user_id', 'category_type_id', 'name']
        for field in required_fields:
            if not category_data.get(field):
                messagebox.showerror("Validation Error", f"Please fill all required fields. Missing: {field}")
                return

        try:
            payload = {
                'user_id': str(category_data['user_id']),
                'category_type_id': str(category_data['category_type_id']),
                'name': category_data['name'],
                'description': category_data.get('description', '')
            }

            response = category_api_client.create_category(payload)

            if response and isinstance(response, dict) and response.get('id'):
                messagebox.showinfo("Success", "Category created successfully!")
                self.controller.show_page("CategoryPage")
            elif response and isinstance(response, dict) and response.get('message'):
                messagebox.showerror("API Error", response.get('message'))
            else:
                error_message = f"Unknown Error. Unexpected API response format: {response}"
                messagebox.showerror("API Error", error_message)

        except ValueError as ve:
            messagebox.showerror("Input Error", f"Please verify input formats. Error: {ve}")
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to create category: {e}")