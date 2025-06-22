import tkinter as tk
from tkinter import ttk, messagebox
from uuid import UUID

from components.list_box_component import ListBoxComponent
from core.category_types_endpoints import category_type_api_client
from core.categories_endpoints import category_api_client
from core.users_endpoints import user_api_client
from pages.base_page import BasePage


class CategoryPage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.category_data = []
        self.users_cache = {}
        self.category_types_cache = {}


    def _setup_ui(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        if self.controller:
            home_button = ttk.Button(self, text="< Back to Home",
                                     command=lambda: self.controller.show_page("HomePage"))
            home_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        else:
            print("Warning: Controller not provided to Categories Page. 'Back to Home' button disabled.")

        title_label = tk.Label(self, text="Categories", font=("Arial", 20, "bold"), pady=10)
        title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

        create_category_button = ttk.Button(self, text="Create New Category",
                                                 command=lambda: self.controller.show_page("CategoryCreatePage"))
        create_category_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        self.columns = ["id", "user_name", "category_type_name", "name", "description", "created_at"]

        self.display_headings = {
            "id": "ID",
            "user_name": "User Name",
            "category_type_name": "Category Type Name",
            "name": "Category Name",
            "description": "Description",
            "created_at": "Created At"
        }

        self.category_list_component = ListBoxComponent(self, columns=self.columns,
                                                             display_headings=self.display_headings)
        self.category_list_component.grid(row=1, column=0, columnspan=2, padx=10, pady=10,
                                               sticky="nsew")
        self.category_list_component.on_select(self._on_category_selected)

        self._load_categories()

    def _fetch_all_users_and_category_types(self):
        try:
            users = user_api_client.get_all_users()
            self.users_cache = {str(user["id"]): user for user in users if user and "id" in user}

            category_types = category_type_api_client.get_all_category_types()
            self.category_types_cache = {str(category_type["id"]): category_type for category_type in category_types if category_type and "id" in category_type}
        except Exception as e:
            messagebox.showwarning("Data Load Warning", f"Could not load all users or Category Types: {e}")


    def _load_categories(self):
        try:
            self._fetch_all_users_and_category_types()
            categories_raw_data = category_api_client.get_all_categories()
            self.category_data = categories_raw_data
            
            items_for_list = []

            for category in categories_raw_data:
                user_id = category.get("user_id")
                category_type_id = category.get("category_type_id")

                category_type_name = self.category_types_cache.get(str(category_type_id), {}).get("name", "Unknown Category Type")
                user_name = self.users_cache.get(str(user_id), {}).get("first_name", "Unknown User")

                row_values = []
                for col in self.columns:
                    if col == "user_name":
                        row_values.append(user_name)
                    elif col == "category_type_name":
                        row_values.append(category_type_name)
                    else:
                        value = category.get(col, '')
                        if isinstance(value, UUID):
                            row_values.append(str(value))
                        else:
                            row_values.append(value)
                items_for_list.append(tuple(row_values))
            self.category_list_component.set_items(items_for_list)
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to load Categories: {e}")
            self.category_list_component.clear_list()

    def _on_category_selected(self, selected_values):
        if selected_values:
            category_id = selected_values[0]
            if self.controller:
                self.controller.show_page("CategoryUpdatePage", category_id=category_id)
            else:
                messagebox.showerror("Error", "Controller not available to show detail page.")
        else:
            pass

    def refresh(self):
        self._load_categories()
