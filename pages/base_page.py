import tkinter as tk
from tkinter import ttk


class BasePage(tk.Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.controller = controller
        self.parent = parent

        style = ttk.Style()
        style.theme_use('clam')

        self.configure(bg="#F0F0F0")

        self._setup_ui()

    def _setup_ui(self):
        raise NotImplementedError("Each page must implement the _setup_ui method.")

    def show(self):
        self.grid(row=0, column=0, sticky="nsew")
        self.tkraise()

    def hide(self):
        self.grid_forget()

    def refresh(self):
        pass
