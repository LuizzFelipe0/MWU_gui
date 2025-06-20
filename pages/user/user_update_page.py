from tkinter import messagebox, ttk
from uuid import UUID

from components.detail_form_component import DetailFormComponent
from core.users_endpoints import user_api_client
from pages.base_page import BasePage


class UserUpdatePage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.current_user_id = None

    def _setup_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        if self.controller:
            back_button = ttk.Button(self, text="< Back to Users",
                                     command=lambda: self.controller.show_page("UserPage"))
            back_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.user_fields_config = [
            {'label': 'ID', 'key': 'id', 'type': 'entry', 'read_only': True},
            {'label': 'First Name', 'key': 'first_name', 'type': 'entry'},
            {'label': 'Last Name', 'key': 'last_name', 'type': 'entry'},
            {'label': 'CPF', 'key': 'cpf', 'type': 'entry'},
            {'label': 'Email', 'key': 'email', 'type': 'entry'},
            {'label': 'Manual Balance', 'key': 'manual_balance', 'type': 'entry'},
            {'label': 'Created At', 'key': 'created_at', 'type': 'entry', 'read_only': True},
            {'label': 'Updated At', 'key': 'updated_at', 'type': 'entry', 'read_only': True},
            {'label': 'Deleted At', 'key': 'deleted_at', 'type': 'entry', 'read_only': True},
        ]

        self.detail_form = DetailFormComponent(
            self,
            fields_config=self.user_fields_config,
            on_save_callback=None,
            on_update_callback=self._update_user,
            on_delete_callback=self._delete_user,
            on_cancel_callback=lambda: self.controller.show_page("UserPage"),
            title_text="Update User Details",
            bg=self.cget('bg')
        )
        self.detail_form.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    def refresh(self, user_id=None):
        if user_id:
            try:
                self.current_user_id = UUID(str(user_id))
                user_data = user_api_client.get_user_by_id(self.current_user_id)
                self.detail_form.set_data(user_data)
                if self.controller:
                    self.controller.title(f"Update User - {user_data.get('first_name', '')}")
            except ValueError:
                messagebox.showerror("Error", f"Invalid User ID format: {user_id}")
                self._reset_form_and_navigate_back()
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to load user details: {e}")
                self._reset_form_and_navigate_back()
        else:
            messagebox.showwarning("Warning", "No user selected for update. Returning to list.")
            self._reset_form_and_navigate_back()  # Always expect an ID for update page

    def _reset_form_and_navigate_back(self):
        self.detail_form.set_data({})
        self.current_user_id = None
        self.controller.show_page("UserPage")

    def _update_user(self):
        if not self.current_user_id:
            messagebox.showerror("Error", "No user selected for update.")
            return

        user_data = self.detail_form.get_data()

        update_fields = ['first_name', 'last_name', 'cpf', 'email', 'manual_balance']
        payload = {k: v for k, v in user_data.items() if k in update_fields and v is not None}

        if 'manual_balance' in payload and payload['manual_balance']:
            try:
                payload['manual_balance'] = float(payload['manual_balance'])
            except ValueError:
                messagebox.showerror("Validation Error", "Manual Balance must be a number.")
                return

        if not payload.get('first_name') or not payload.get('email') or not payload.get('cpf'):
            messagebox.showerror("Validation Error", "First Name, CPF, and Email are required.")
            return

        try:
            user_api_client.update_user(self.current_user_id, payload)
            messagebox.showinfo("Success", "User updated successfully!")
            self.controller.show_page("UserPage")
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to update user: {e}")

    def _delete_user(self):
        if not self.current_user_id:
            messagebox.showerror("Error", "No user selected for deletion.")
            return

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user ID {self.current_user_id}?"):
            try:
                user_api_client.delete_user(self.current_user_id)
                messagebox.showinfo("Success", "User deleted successfully (soft delete)!")
                self.controller.show_page("UserPage")
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to delete user: {e}")
