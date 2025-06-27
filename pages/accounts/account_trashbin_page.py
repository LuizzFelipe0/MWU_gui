import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
from uuid import UUID
from typing import Optional

from components.list_box_component import ListBoxComponent
from core.accounts_endpoints import account_api_client
from pages.base_page import BasePage


class AccountsTrashbinPage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.account_data = []
        self.selected_account_id: Optional[UUID] = None

    def _setup_ui(self):
        self._setup_grid_configuration()
        self._create_navigation_button()
        self._create_title_label()
        self._create_action_buttons()
        self._create_list_component()
        self._load_accounts()

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
                text="< Back to Accounts",
                command=lambda: self.controller.show_page("AccountsPage")
            ).grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    def _create_title_label(self):
        tk.Label(
            self,
            text="Accounts Trash-Bin",
            font=("Arial", 20, "bold"),
            pady=10
        ).grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

    def _create_action_buttons(self):
        button_frame = tk.Frame(self, bg=self.cget('bg'))
        button_frame.grid(row=1, column=0, columnspan=2, pady=(0, 10), sticky="e")

        self.restore_button = ttk.Button(
            button_frame,
            text="Restore Account",
            state="disabled",
            command=self._restore_selected_account
        )
        self.restore_button.pack(side="left", padx=(0, 10))

        self.force_delete_button = ttk.Button(
            button_frame,
            text="Force Delete",
            state="disabled",
            command=self._force_delete_selected_account
        )
        self.force_delete_button.pack(side="left")

    def _create_list_component(self):
        self.columns = ["id", "name", "type", "account_number", "created_at", "updated_at", "deleted_at"]
        self.display_headings = {
            "id": "ID",
            "name": "Name",
            "type": "Type",
            "account_number": "Account Number",
            "created_at": "Created At",
            "updated_at": "Updated At",
            "deleted_at": "Deleted At"
        }

        self.account_list_component = ListBoxComponent(
            self,
            columns=self.columns,
            display_headings=self.display_headings
        )
        self.account_list_component.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew"
        )
        self.account_list_component.on_select(self._on_account_selected)

    def _on_account_selected(self, selected_values):
        if selected_values:
            try:
                self.selected_account_id = UUID(selected_values[0])
                self.restore_button.config(state="normal")
                self.force_delete_button.config(state="normal")
            except ValueError:
                self._clear_selection()
        else:
            self._clear_selection()

    def _clear_selection(self):
        self.selected_account_id = None
        self.restore_button.config(state="disabled")
        self.force_delete_button.config(state="disabled")

    def _restore_selected_account(self):
        if not self.selected_account_id:
            return

        if messagebox.askyesno(
            "Confirm Restore",
            f"Are you sure you want to restore account ID {self.selected_account_id}?"
        ):
            try:
                account_api_client.restore_account(self.selected_account_id)
                messagebox.showinfo("Success", "Account restored successfully!")
                self.refresh()
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to restore account: {e}")
            finally:
                self._clear_selection()

    def _force_delete_selected_account(self):
        if not self.selected_account_id:
            return

        if messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to PERMANENTLY delete account ID {self.selected_account_id}?\n"
            "This action cannot be undone!"
        ):
            try:
                account_api_client.force_delete_account(self.selected_account_id)
                messagebox.showinfo("Success", "Account permanently deleted!")
                self.refresh()
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to delete account: {e}")
            finally:
                self._clear_selection()

    def _load_accounts(self):
        try:
            accounts_raw_data = account_api_client.get_deleted_accounts()
            self.account_data = accounts_raw_data
            items_for_list = []
            for account in accounts_raw_data:
                row_values = []
                for col in self.columns:
                    value = account.get(col, '')
                    if isinstance(value, UUID):
                        row_values.append(str(value))
                    elif isinstance(value, datetime):
                        row_values.append(value.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        row_values.append(value)
                items_for_list.append(tuple(row_values))
            self.account_list_component.set_items(items_for_list)
            self._clear_selection()
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to load Accounts: {e}")
            self.account_list_component.clear_list()

    def refresh(self):
        self._load_accounts()