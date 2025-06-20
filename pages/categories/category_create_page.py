from tkinter import messagebox, ttk

from ...components.detail_form_component import DetailFormComponent
from ...core.category_types_endpoints import category_type_api_client
from ...pages.base_page import BasePage


class CategoryCreatePage(BasePage):
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
            back_button = ttk.Button(self, text="< Back to Categorys",
                                     command=lambda: self.controller.show_page("CategorysPage"))
            back_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.category_type_fields_config = [
            {'label': 'Name', 'key': 'name', 'type': 'entry'},
            {'label': 'Is Positive', 'key': 'is_positive', 'type': 'dropdown',
             'options': ['True', 'False']},
        ]

        self.detail_form = DetailFormComponent(
            self,
            fields_config=self.category_type_fields_config,
            on_save_callback=self._create_category_type,
            on_update_callback=None,
            on_delete_callback=None,
            on_cancel_callback=lambda: self.controller.show_page("CategorysPage"),
            title_text="Create New Category",
            bg=self.cget('bg')
        )
        self.detail_form.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    def refresh(self, **kwargs):

        self.detail_form.set_data({})
        if self.controller:
            self.controller.title("Create New Category")

    def _create_category_type(self):
        category_type_data = self.detail_form.get_data()

        input_fields = ['name', 'is_positive']
        payload = {k: v for k, v in category_type_data.items() if k in input_fields and v is not None}

        if payload.get('is_positive') not in ['True', 'False']:
            messagebox.showerror("Validation Error", "Please select a valid is_positive value.")
            return

        if not payload.get('name') or not payload.get('is_positive'):
            messagebox.showerror("Validation Error", "Name and Is Positive are required.")
            return

        try:
            category_type_api_client.create_category_type(payload)
            messagebox.showinfo("Success", "Category created successfully!")
            self.controller.show_page("CategorysPage")
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to create category_type: {e}")
