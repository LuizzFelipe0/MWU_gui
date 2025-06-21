import tkinter as tk
from tkinter import ttk
from datetime import datetime
from components.id_dropdown_component import IdDropdownComponent


class DetailFormComponent(tk.Frame):
    def __init__(self, parent, fields_config: list,
                 on_save_callback=None, on_update_callback=None,
                 on_delete_callback=None, on_cancel_callback=None,
                 title_text="Details of Object", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.fields_config = fields_config
        self.on_save_callback = on_save_callback
        self.on_update_callback = on_update_callback
        self.on_delete_callback = on_delete_callback
        self.on_cancel_callback = on_cancel_callback
        self.title_text = title_text

        self.entry_vars = {}
        self.id_dropdown_components = {}

        self._setup_ui()
        self._apply_styles()

    def _apply_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Detail.TLabel",
                        font=("Arial", 11),
                        foreground="#333333")

        style.configure("Detail.TEntry",
                        fieldbackground="white",
                        foreground="#333333",
                        padding=(8, 8),
                        borderwidth=1,
                        relief="flat")
        style.map("Detail.TEntry",
                  fieldbackground=[("focus", "#E0F2F7")])

        style.configure("Detail.TCombobox",
                        fieldbackground="white",
                        foreground="#333333",
                        padding=(8, 8),
                        borderwidth=1,
                        relief="flat")
        style.map("Detail.TCombobox",
                  fieldbackground=[("focus", "#E0F2F7")])

        style.configure("Save.TButton", background="#007AFF", foreground="white", font=("Arial", 12, "bold"),
                        borderwidth=0, relief="flat")
        style.map("Save.TButton", background=[("active", "#0056B3"), ("!disabled", "#007AFF")],
                  foreground=[("active", "white"), ("!disabled", "white")])
        style.configure("Update.TButton", background="#34C759", foreground="white", font=("Arial", 12, "bold"),
                        borderwidth=0, relief="flat")
        style.map("Update.TButton", background=[("active", "#28A745"), ("!disabled", "#34C759")],
                  foreground=[("active", "white"), ("!disabled", "white")])
        style.configure("Delete.TButton", background="#FF3B30", foreground="white", font=("Arial", 12, "bold"),
                        borderwidth=0, relief="flat")
        style.map("Delete.TButton", background=[("active", "#CC2D25"), ("!disabled", "#FF3B30")],
                  foreground=[("active", "white"), ("!disabled", "white")])
        style.configure("Cancel.TButton", background="#8E8E93", foreground="white", font=("Arial", 12, "bold"),
                        borderwidth=0, relief="flat")
        style.map("Cancel.TButton", background=[("active", "#707073"), ("!disabled", "#8E8E93")],
                  foreground=[("active", "white"), ("!disabled", "white")])

    def _setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)

        title_label = tk.Label(self, text=self.title_text, font=("Arial", 18, "bold"), pady=15)
        title_label.grid(row=0, column=0, columnspan=3, sticky="n", pady=(10, 20))

        current_row = 1
        for field in self.fields_config:
            label_text = field.get('label', '')
            field_key = field.get('key', '')
            field_type = field.get('type', 'entry')
            read_only = field.get('read_only', False)
            show_field = field.get('show', True)
            options = field.get('options', [])

            if not show_field:
                continue

            ttk.Label(self, text=f"{label_text}:", style="Detail.TLabel").grid(row=current_row, column=0, padx=10,
                                                                               pady=5, sticky="w")

            if field_type == 'entry' or field_type == 'password':
                var = tk.StringVar(value="")
                widget = ttk.Entry(self, textvariable=var, show="*" if field_type == 'password' else "",
                                   style="Detail.TEntry")
                if read_only:
                    widget.configure(state="readonly")
                self.entry_vars[field_key] = var
                widget.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            elif field_type == 'dropdown':
                var = tk.StringVar(value="")
                widget = ttk.Combobox(self, textvariable=var, values=options, state="readonly",
                                      style="Detail.TCombobox")
                if read_only:
                    widget.configure(state="readonly")
                self.entry_vars[field_key] = var
                widget.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")
            elif field_type == 'id_dropdown':
                widget = IdDropdownComponent(self, style="Detail.TCombobox")
                widget.set_options(options)
                if read_only:
                    widget.configure(state="readonly")
                self.id_dropdown_components[field_key] = widget
                widget.grid(row=current_row, column=1, padx=10, pady=5, sticky="ew")

            current_row += 1

        tk.Frame(self, height=20).grid(row=current_row, column=0, columnspan=3)
        current_row += 1

        button_frame = tk.Frame(self)
        button_frame.grid(row=current_row, column=0, columnspan=3, pady=10)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=0)
        button_frame.grid_columnconfigure(2, weight=0)
        button_column_start = 1

        if self.on_save_callback:
            ttk.Button(button_frame, text="Save", command=self.on_save_callback, style="Save.TButton").grid(row=0,
                                                                                                            column=button_column_start,
                                                                                                            padx=5,
                                                                                                            pady=5)
            button_column_start += 1
        if self.on_update_callback:
            ttk.Button(button_frame, text="Update", command=self.on_update_callback, style="Update.TButton").grid(row=0,
                                                                                                                  column=button_column_start,
                                                                                                                  padx=5,
                                                                                                                  pady=5)
            button_column_start += 1
        if self.on_delete_callback:
            ttk.Button(button_frame, text="Delete", command=self.on_delete_callback, style="Delete.TButton").grid(row=0,
                                                                                                                  column=button_column_start,
                                                                                                                  padx=5,
                                                                                                                  pady=5)
            button_column_start += 1
        if self.on_cancel_callback:
            ttk.Button(button_frame, text="Cancel", command=self.on_cancel_callback, style="Cancel.TButton").grid(row=0,
                                                                                                                  column=button_column_start,
                                                                                                                  padx=5,
                                                                                                                  pady=5)

    def set_data(self, data: dict):
        for field in self.fields_config:
            field_key = field.get('key', '')
            field_type = field.get('type', 'entry')

            value = data.get(field_key, "")

            if field_type == 'id_dropdown':
                component = self.id_dropdown_components.get(field_key)
                if component:
                    component.set_selected_id(str(value))
            else:
                var = self.entry_vars.get(field_key)
                if var:
                    if isinstance(value, datetime):
                        var.set(value.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        var.set(str(value))

    def get_data(self) -> dict:
        data = {}
        for key, var in self.entry_vars.items():
            data[key] = var.get()

        for key, component in self.id_dropdown_components.items():
            data[key] = component.get_selected_id()
        return data