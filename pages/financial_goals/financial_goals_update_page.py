from tkinter import messagebox, ttk
from uuid import UUID

from ...components.detail_form_component import DetailFormComponent
from ...core.categories_endpoints import category_api_client
from ...pages.base_page import BasePage


class CategoryUpdatePage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.current_category_id = None

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
            {'label': 'ID', 'key': 'id', 'type': 'entry', 'read_only': True},
            {'label': 'Name', 'key': 'name', 'type': 'entry'},
            {'label': 'Is Positive', 'key': 'is_positive', 'type': 'dropdown',
             'options': ['True', 'False']},
        ]

        self.detail_form = DetailFormComponent(
            self,
            fields_config=self.category_fields_config,
            on_save_callback=None,
            on_update_callback=self._update_category,
            on_delete_callback=self._delete_category,
            on_cancel_callback=lambda: self.controller.show_page("CategoryPage"),
            title_text="Update Category Details",
            bg=self.cget('bg')
        )
        self.detail_form.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    def refresh(self, category_id=None):
        if category_id:
            try:
                self.current_category_id = UUID(str(category_id))
                category_data = category_api_client.get_category_by_id(self.current_category_id)
                self.detail_form.set_data(category_data)
                if self.controller:
                    self.controller.title(f"Update Category - {category_data.get('name', '')}")
            except ValueError:
                messagebox.showerror("Error", f"Invalid Category ID format: {category_id}")
                self._reset_form_and_navigate_back()
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to load category details: {e}")
                self._reset_form_and_navigate_back()
        else:
            messagebox.showwarning("Warning", "No category selected for update. Returning to list.")
            self._reset_form_and_navigate_back()

    def _reset_form_and_navigate_back(self):
        self.detail_form.set_data({})
        self.current_category_id = None
        self.controller.show_page("CategoryPage")

    def _update_category(self):
        if not self.current_category_id:
            messagebox.showerror("Error", "No category selected for update.")
            return

        category_data = self.detail_form.get_data()

        update_fields = ['name', 'is_positive']
        payload = {k: v for k, v in category_data.items() if k in update_fields and v is not None}

        if payload.get('is_positive') not in ['True', 'False']:
            messagebox.showerror("Validation Error", "Please select a valid is_positive value.")
            return

        if not payload.get('name') or not payload.get('is_positive'):
            messagebox.showerror("Validation Error", "Name and Is Positive are required.")
            return

        try:
            category_api_client.update_category(self.current_category_id, payload)
            messagebox.showinfo("Success", "Category updated successfully!")
            self.controller.show_page("CategoryPage")
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to update Category: {e}")

    def _delete_category(self):
        if not self.current_category_id:
            messagebox.showerror("Error", "No Category selected for deletion.")
            return

        if messagebox.askyesno("Confirm Delete",
                               f"Are you sure you want to delete category ID {self.current_category_id}?"):
            try:
                category_api_client.delete_category(self.current_category_id)
                messagebox.showinfo("Success",
                                    "Category deleted successfully!")
                self.controller.show_page("CategoryPage")
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to delete Category: {e}")
