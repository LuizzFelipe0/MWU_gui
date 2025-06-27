import tkinter as tk
from tkinter import ttk, messagebox
from uuid import UUID
from typing import Optional

from components.list_box_component import ListBoxComponent
from core.transactions_endpoints import transaction_api_client
from core.categories_endpoints import category_api_client
from core.users_endpoints import user_api_client
from pages.base_page import BasePage


class TransactionTrashbinPage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.Transaction_data = []
        self.users_cache = {}
        self.categories_cache = {}
        self.selected_transaction_id: Optional[UUID] = None

    def _setup_ui(self):
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        if self.controller:
            ttk.Button(
                self,
                text="< Back to Transactions",
                command=lambda: self.controller.show_page("TransactionPage")
            ).grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        tk.Label(
            self,
            text="Transactions Trash-Bin",
            font=("Arial", 20, "bold"),
            pady=10
        ).grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

        button_frame = tk.Frame(self, bg=self.cget('bg'))
        button_frame.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="e")

        self.restore_button = ttk.Button(
            button_frame,
            text="Restore Transaction",
            state="disabled",
            command=self._restore_selected_transaction
        )
        self.restore_button.pack(side="left", padx=(0, 10))

        self.force_delete_button = ttk.Button(
            button_frame,
            text="Force Delete",
            state="disabled",
            command=self._force_delete_selected_transaction
        )
        self.force_delete_button.pack(side="left")

        self.columns = ["id", "user_name", "category_name", "name", "amount", "date", "is_recurring"]
        self.display_headings = {
            "id": "ID",
            "user_name": "User Name",
            "category_name": "Category Name",
            "name": "Name",
            "amount": "Amount",
            "date": "Date",
            "is_recurring": "Is Recurring"
        }

        self.transaction_list_component = ListBoxComponent(
            self,
            columns=self.columns,
            display_headings=self.display_headings
        )
        self.transaction_list_component.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew"
        )
        self.transaction_list_component.on_select(self._on_transaction_selected)
        self._load_transactions()

    def _on_transaction_selected(self, selected_values):
        if selected_values:
            try:
                self.selected_transaction_id = UUID(selected_values[0])
                self.restore_button.config(state="normal")
                self.force_delete_button.config(state="normal")
            except ValueError:
                self._clear_selection()
        else:
            self._clear_selection()

    def _clear_selection(self):
        self.selected_transaction_id = None
        self.restore_button.config(state="disabled")
        self.force_delete_button.config(state="disabled")

    def _restore_selected_transaction(self):
        if not self.selected_transaction_id:
            return

        if messagebox.askyesno(
                "Confirm Restore",
                f"Are you sure you want to restore transaction ID {self.selected_transaction_id}?"
        ):
            try:
                transaction_api_client.restore_transaction(self.selected_transaction_id)
                messagebox.showinfo("Success", "Transaction restored successfully!")
                self.refresh()
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to restore transaction: {e}")
            finally:
                self._clear_selection()

    def _force_delete_selected_transaction(self):
        if not self.selected_transaction_id:
            return

        if messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to PERMANENTLY delete transaction ID {self.selected_transaction_id}?\n"
                "This action cannot be undone!"
        ):
            try:
                transaction_api_client.force_delete_transaction(self.selected_transaction_id)
                messagebox.showinfo("Success", "Transaction permanently deleted!")
                self.refresh()
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to delete transaction: {e}")
            finally:
                self._clear_selection()

    def _fetch_all_users_and_categories(self):
        try:
            users = user_api_client.get_all_users()
            self.users_cache = {str(user["id"]): user for user in users if user and "id" in user}

            categories = category_api_client.get_all_categories()
            self.categories_cache = {str(category["id"]): category for category in categories if
                                     category and "id" in category}
        except Exception as e:
            messagebox.showwarning("Data Load Warning", f"Could not load all users or categories: {e}")

    def _load_transactions(self):
        try:
            self._fetch_all_users_and_categories()
            transactions_raw_data = transaction_api_client.get_deleted_transactions()
            self.Transaction_data = transactions_raw_data

            items_for_list = []
            for transaction in transactions_raw_data:
                user_id = transaction.get("user_id")
                category_id = transaction.get("category_id")

                category_name = self.categories_cache.get(str(category_id), {}).get("name", "Unknown Category")
                user_name = self.users_cache.get(str(user_id), {}).get("first_name", "Unknown User")

                row_values = []
                for col in self.columns:
                    if col == "user_name":
                        row_values.append(user_name)
                    elif col == "category_name":
                        row_values.append(category_name)
                    else:
                        value = transaction.get(col, '')
                        row_values.append(str(value) if isinstance(value, UUID) else value)
                items_for_list.append(tuple(row_values))

            self.transaction_list_component.set_items(items_for_list)
            self._clear_selection()
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to load Transactions: {e}")
            self.transaction_list_component.clear_list()

    def refresh(self):
        self._load_transactions()