import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from uuid import UUID

from components.list_box_component import ListBoxComponent
from core.category_types_endpoints import category_type_api_client
from pages.base_page import BasePage


class CategoryTypesPage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.category_type_data = []

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
            print("Warning: Controller not provided to CategoryTypesPage. 'Back to Home' button disabled.")

        title_label = tk.Label(self, text="Category Types", font=("Arial", 20, "bold"), pady=10)
        title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

        create_category_type_button = ttk.Button(self, text="Create New Category Type",
                                        command=lambda: self.controller.show_page("CategoryTypeCreatePage"))
        create_category_type_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        self.columns = ["id", "name", "is_positive"]

        self.display_headings = {
            "id": "ID",
            "name": "Name",
            "is_positive": "Is Positive",
        }

        self.category_type_list_component = ListBoxComponent(self, columns=self.columns, display_headings=self.display_headings)
        self.category_type_list_component.grid(row=1, column=0, columnspan=2, padx=10, pady=10,
                                      sticky="nsew")
        self.category_type_list_component.on_select(self._on_category_type_selected)

        refresh_button = ttk.Button(self, text="Refresh Category Types", command=self._load_category_types)
        refresh_button.grid(row=2, column=0, columnspan=2, pady=5)

        self._load_category_types()

    def _load_category_types(self):
        try:
            category_types_raw_data = category_type_api_client.get_all_category_types()
            self.category_type_data = category_types_raw_data
            items_for_list = []
            for category_type in category_types_raw_data:
                row_values = []
                for col in self.columns:
                    value = category_type.get(col, '')
                    if isinstance(value, UUID):
                        row_values.append(str(value))
                    elif isinstance(value, datetime):
                        row_values.append(value.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        row_values.append(value)
                items_for_list.append(tuple(row_values))
            self.category_type_list_component.set_items(items_for_list)
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to load Category Types: {e}")
            self.category_type_list_component.clear_list()

    def _on_category_type_selected(self, selected_values):
        if selected_values:
            category_type_id = selected_values[0]
            if self.controller:
                self.controller.show_page("CategoryTypeUpdatePage", category_type_id=category_type_id)
            else:
                messagebox.showerror("Error", "Controller not available to show detail page.")
        else:
            pass

    def refresh(self):
        self._load_category_types()
