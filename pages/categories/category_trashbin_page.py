import tkinter as tk
from tkinter import ttk, messagebox
from uuid import UUID
from typing import Optional

from components.list_box_component import ListBoxComponent
from core.category_types_endpoints import category_type_api_client
from core.categories_endpoints import category_api_client
from core.users_endpoints import user_api_client
from pages.base_page import BasePage


class CategoryTrashbinPage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.category_data = []
        self.users_cache = {}
        self.category_types_cache = {}
        self.selected_category_id: Optional[UUID] = None

    def _setup_ui(self):
        self._setup_grid_configuration()
        self._create_navigation_button()
        self._create_title_label()
        self._create_action_buttons()
        self._create_list_component()
        self._load_categories()

    def _setup_grid_configuration(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

    def _create_navigation_button(self):
        if self.controller:
            ttk.Button(
                self,
                text="< Back to Categories",
                command=lambda: self.controller.show_page("CategoryPage")
            ).grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    def _create_title_label(self):
        tk.Label(
            self,
            text="Categories Trash-Bin",
            font=("Arial", 20, "bold"),
            pady=10
        ).grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

    def _create_action_buttons(self):
        button_frame = tk.Frame(self, bg=self.cget('bg'))
        button_frame.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="e")

        self.restore_button = ttk.Button(
            button_frame,
            text="Restore Category",
            state="disabled",
            command=self._restore_selected_category
        )
        self.restore_button.pack(side="left", padx=(0, 10))

        self.force_delete_button = ttk.Button(
            button_frame,
            text="Force Delete",
            state="disabled",
            command=self._force_delete_selected_category
        )
        self.force_delete_button.pack(side="left")

    def _create_list_component(self):
        self.columns = ["id", "user_name", "category_type_name", "name", "description", "created_at"]

        self.display_headings = {
            "id": "ID",
            "user_name": "User Name",
            "category_type_name": "Category Type Name",
            "name": "Category Name",
            "description": "Description",
            "created_at": "Created At"
        }

        self.category_list_component = ListBoxComponent(
            self,
            columns=self.columns,
            display_headings=self.display_headings
        )
        self.category_list_component.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew"
        )
        self.category_list_component.on_select(self._on_category_selected)

    def _on_category_selected(self, selected_values):
        if selected_values:
            try:
                self.selected_category_id = UUID(selected_values[0])
                self.restore_button.config(state="normal")
                self.force_delete_button.config(state="normal")
            except ValueError:
                self._clear_selection()
        else:
            self._clear_selection()

    def _clear_selection(self):
        self.selected_category_id = None
        self.restore_button.config(state="disabled")
        self.force_delete_button.config(state="disabled")

    def _restore_selected_category(self):
        if not self.selected_category_id:
            return

        if messagebox.askyesno(
                "Confirm Restore",
                f"Are you sure you want to restore category ID {self.selected_category_id}?"
        ):
            try:
                response = category_api_client.restore_category(self.selected_category_id)
                if response:
                    messagebox.showinfo("Success", "Category restored successfully!")
                    self.refresh()
                else:
                    messagebox.showerror("Error", "Failed to restore category")
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to restore category: {e}")
            finally:
                self._clear_selection()

    def _force_delete_selected_category(self):
        if not self.selected_category_id:
            return

        if messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to PERMANENTLY delete category ID {self.selected_category_id}?\n"
                "This action cannot be undone!"
        ):
            try:
                category_api_client.force_delete_category(self.selected_category_id)
                messagebox.showinfo("Success", "Category permanently deleted!")
                self.refresh()
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to delete category: {e}")
            finally:
                self._clear_selection()

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

    def _load_categories(self):
        try:
            self._fetch_all_users_and_category_types()
            categories_raw_data = category_api_client.get_deleted_categories()
            self.category_data = categories_raw_data

            items_for_list = []
            for category in categories_raw_data:
                user_id = category.get("user_id")
                category_type_id = category.get("category_type_id")

                category_type_name = self.category_types_cache.get(
                    str(category_type_id), {}
                ).get("name", "Unknown Category Type")

                user_name = self.users_cache.get(
                    str(user_id), {}
                ).get("first_name", "Unknown User")

                row_values = []
                for col in self.columns:
                    if col == "user_name":
                        row_values.append(user_name)
                    elif col == "category_type_name":
                        row_values.append(category_type_name)
                    else:
                        value = category.get(col, '')
                        row_values.append(str(value) if isinstance(value, UUID) else value)

                items_for_list.append(tuple(row_values))

            self.category_list_component.set_items(items_for_list)
            self._clear_selection()

        except Exception as e:
            messagebox.showerror("API Error", f"Failed to load Categories: {e}")
            self.category_list_component.clear_list()

    def refresh(self):
        self._load_categories()