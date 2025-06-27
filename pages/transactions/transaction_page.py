import tkinter as tk
from tkinter import ttk, messagebox
from uuid import UUID

from components.list_box_component import ListBoxComponent
from core.transactions_endpoints import transaction_api_client
from core.categories_endpoints import category_api_client
from core.users_endpoints import user_api_client
from pages.base_page import BasePage


class TransactionPage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.Transaction_data = []
        self.users_cache = {}
        self.categories_cache = {}

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
            print("Warning: Controller not provided to Transactions Page. 'Back to Home' button disabled.")

        title_label = tk.Label(self, text="Transactions", font=("Arial", 20, "bold"), pady=10)
        title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

        button_frame = tk.Frame(self, bg=self.cget('bg'))
        button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        transaction_trashbin_button = ttk.Button(button_frame, text="Transactions Trash Bin",
                                              command=lambda: self.controller.show_page(
                                                  "TransactionTrashbinPage"))
        transaction_trashbin_button.pack(side="left", padx=(0, 20))

        create_transaction_button = ttk.Button(button_frame, text="Create New Transaction",
                                            command=lambda: self.controller.show_page("TransactionCreatePage"))
        create_transaction_button.pack(side="left")

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

        self.transaction_list_component = ListBoxComponent(self, columns=self.columns,
                                                             display_headings=self.display_headings)
        self.transaction_list_component.grid(row=1, column=0, columnspan=2, padx=10, pady=10,
                                               sticky="nsew")
        self.transaction_list_component.on_select(self._on_transaction_selected)

        self._load_transactions()

    def _fetch_all_users_and_categories(self):
        try:
            users = user_api_client.get_all_users()
            self.users_cache = {str(user["id"]): user for user in users if user and "id" in user}

            categories = category_api_client.get_all_categories()
            self.categories_cache = {str(category["id"]): category for category in categories if category and "id" in category}
        except Exception as e:
            messagebox.showwarning("Data Load Warning", f"Could not load all users or categories: {e}")


    def _load_transactions(self):
        try:
            self._fetch_all_users_and_categories()
            transations_raw_data = transaction_api_client.get_all_transactions()
            self.Transaction_data = transations_raw_data
            
            items_for_list = []

            for Transaction in transations_raw_data:
                user_id = Transaction.get("user_id")
                category_id = Transaction.get("category_id")

                category_name = self.categories_cache.get(str(category_id), {}).get("name", "Unknown Category")
                user_name = self.users_cache.get(str(user_id), {}).get("first_name", "Unknown User")

                row_values = []
                for col in self.columns:
                    if col == "user_name":
                        row_values.append(user_name)
                    elif col == "category_name":
                        row_values.append(category_name)
                    else:
                        value = Transaction.get(col, '')
                        if isinstance(value, UUID):
                            row_values.append(str(value))
                        else:
                            row_values.append(value)
                items_for_list.append(tuple(row_values))
            self.transaction_list_component.set_items(items_for_list)
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to load Transactions: {e}")
            self.transaction_list_component.clear_list()

    def _on_transaction_selected(self, selected_values):
        if selected_values:
            transaction_id = selected_values[0]
            if self.controller:
                self.controller.show_page("TransactionUpdatePage", transaction_id=transaction_id)
            else:
                messagebox.showerror("Error", "Controller not available to show detail page.")
        else:
            pass

    def refresh(self):
        self._load_transactions()
