from tkinter import messagebox, ttk
from uuid import UUID

from components.detail_form_component import DetailFormComponent
from core.category_types_endpoints import category_type_api_client
from pages.base_page import BasePage


class CategoryTypeUpdatePage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.current_category_type_id = None

    def _setup_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        if self.controller:
            back_button = ttk.Button(self, text="< Back to Category Types",
                                     command=lambda: self.controller.show_page("CategoryTypesPage"))
            back_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.category_type_fields_config = [
            {'label': 'ID', 'key': 'id', 'type': 'entry', 'read_only': True},
            {'label': 'Name', 'key': 'name', 'type': 'entry'},
            {'label': 'Is Positive', 'key': 'is_positive', 'type': 'dropdown',
             'options': ['True', 'False']},
        ]

        self.detail_form = DetailFormComponent(
            self,
            fields_config=self.category_type_fields_config,
            on_save_callback=None,
            on_update_callback=self._update_category_type,
            on_delete_callback=self._delete_category_type,
            on_cancel_callback=lambda: self.controller.show_page("CategoryTypesPage"),
            title_text="Update Category Type Details",
            bg=self.cget('bg')
        )
        self.detail_form.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    def refresh(self, category_type_id=None):
        if category_type_id:
            try:
                self.current_category_type_id = UUID(str(category_type_id))
                category_type_data = category_type_api_client.get_category_type_by_id(self.current_category_type_id)
                self.detail_form.set_data(category_type_data)
                if self.controller:
                    self.controller.title(f"Update Category Type - {category_type_data.get('name', '')}")
            except ValueError:
                messagebox.showerror("Error", f"Invalid Category Type ID format: {category_type_id}")
                self._reset_form_and_navigate_back()
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to load category_type details: {e}")
                self._reset_form_and_navigate_back()
        else:
            messagebox.showwarning("Warning", "No category_type selected for update. Returning to list.")
            self._reset_form_and_navigate_back()

    def _reset_form_and_navigate_back(self):
        self.detail_form.set_data({})
        self.current_category_type_id = None
        self.controller.show_page("CategoryTypesPage")

    def _update_category_type(self):
        if not self.current_category_type_id:
            messagebox.showerror("Error", "No category_type selected for update.")
            return

        category_type_data = self.detail_form.get_data()

        update_fields = ['name', 'is_positive']
        payload = {k: v for k, v in category_type_data.items() if k in update_fields and v is not None}

        if payload.get('is_positive') not in ['True', 'False']:
            messagebox.showerror("Validation Error", "Please select a valid is_positive value.")
            return

        if not payload.get('name') or not payload.get('is_positive'):
            messagebox.showerror("Validation Error", "Name and Is Positive are required.")
            return

        try:
            category_type_api_client.update_category_type(self.current_category_type_id, payload)
            messagebox.showinfo("Success", "Category Type updated successfully!")
            self.controller.show_page("CategoryTypesPage")
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to update Category Type: {e}")

    def _delete_category_type(self):
        if not self.current_category_type_id:
            messagebox.showerror("Error", "No Category Type selected for deletion.")
            return

        if messagebox.askyesno("Confirm Delete",
                               f"Are you sure you want to delete category_type ID {self.current_category_type_id}?"):
            try:
                category_type_api_client.delete_category_type(self.current_category_type_id)
                messagebox.showinfo("Success",
                                    "Category Type deleted successfully!")
                self.controller.show_page("CategoryTypesPage")
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to delete Category Type: {e}")
