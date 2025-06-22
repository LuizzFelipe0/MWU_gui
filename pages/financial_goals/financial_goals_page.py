import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from uuid import UUID

from components.list_box_component import ListBoxComponent
from core.financial_goals_endpoints import financial_goals_api_client
from core.users_endpoints import user_api_client
from pages.base_page import BasePage


class FinancialGoalsPage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.financial_goal_data = []
        self.users_cache = {}

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
            print("Warning: Controller not provided to Financial Goals Page. 'Back to Home' button disabled.")

        title_label = tk.Label(self, text="Financial Goals", font=("Arial", 20, "bold"), pady=10)
        title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

        create_financial_goal_button = ttk.Button(self, text="Create New FinancialGoal",
                                                 command=lambda: self.controller.show_page("FinancialGoalsCreatePage"))
        create_financial_goal_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        self.columns = ["id", "user_name", "name", "description", "target_amount", "deadline", "created_at"]

        self.display_headings = {
            "id": "ID",
            "user_name": "User Name",
            "name": "Name",
            "description": "Description",
            "target_amount": "Target Amount",
            "deadline": "Deadline",
            "created_at": "Created At"
        }

        self.financial_goal_list_component = ListBoxComponent(self, columns=self.columns,
                                                             display_headings=self.display_headings)
        self.financial_goal_list_component.grid(row=1, column=0, columnspan=2, padx=10, pady=10,
                                               sticky="nsew")
        self.financial_goal_list_component.on_select(self._on_financial_goal_selected)

        self._load_financial_goals()

    def _fetch_all_users(self):
        try:
            users = user_api_client.get_all_users()
            self.users_cache = {str(user["id"]): user for user in users if user and "id" in user}
        except Exception as e:
            messagebox.showwarning("Data Load Warning", f"Could not load all users: {e}")


    def _load_financial_goals(self):
        try:
            self._fetch_all_users()
            financial_goals_raw_data = financial_goals_api_client.get_all_financial_goals()
            self.financial_goal_data = financial_goals_raw_data
            items_for_list = []

            for financial_goal in financial_goals_raw_data:
                user_id = financial_goal.get("user_id")
                user_name = self.users_cache.get(str(user_id), {}).get("first_name", "Unknown User")

                row_values = []
                for col in self.columns:
                    if col == "user_name":
                        row_values.append(user_name)
                    else:
                        value = financial_goal.get(col, '')
                        if isinstance(value, UUID):
                            row_values.append(str(value))
                        else:
                            row_values.append(value)
                items_for_list.append(tuple(row_values))
            self.financial_goal_list_component.set_items(items_for_list)
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to load Financial Goals: {e}")
            self.financial_goal_list_component.clear_list()

    def _on_financial_goal_selected(self, selected_values):
        if selected_values:
            financial_goal_id = selected_values[0]
            if self.controller:
                self.controller.show_page("FinancialGoalsUpdatePage", financial_goals_id=financial_goal_id)
            else:
                messagebox.showerror("Error", "Controller not available to show detail page.")
        else:
            pass

    def refresh(self):
        self._load_financial_goals()
