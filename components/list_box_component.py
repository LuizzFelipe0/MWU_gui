import tkinter as tk
from tkinter import ttk


class ListBoxComponent(tk.Frame):
    def __init__(self, parent, columns: list, display_headings: dict, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.columns = columns
        self.display_headings = display_headings

        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Treeview",
                        background="#FFFFFF",
                        foreground="#333333",
                        rowheight=28,
                        fieldbackground="#FFFFFF",
                        borderwidth=0, relief="flat")

        style.configure("Treeview.Heading",
                        font=("Arial", 10, "bold"),
                        background="#E0E0E0",
                        foreground="#555555",
                        relief="flat",
                        padding=(5, 5))

        style.map("Treeview",
                  background=[("selected", "#007AFF")],
                  foreground=[("selected", "white")])

        style.configure("Vertical.TScrollbar",
                        troughcolor="#F0F0F0",
                        background="#C0C0C0",
                        bordercolor="#E0E0E0",
                        arrowcolor="#888888",
                        relief="flat")
        style.configure("Horizontal.TScrollbar",
                        troughcolor="#F0F0F0",
                        background="#C0C0C0",
                        bordercolor="#E0E0E0",
                        arrowcolor="#888888",
                        relief="flat")

        self._setup_ui()

    def _setup_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=self.display_headings.get(col, col))
            self.tree.column(col, anchor="center")

        scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        scrollbar_x = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview, style="Horizontal.TScrollbar")
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

    def clear_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def add_item(self, item_values: tuple):
        self.tree.insert("", "end", values=item_values)

    def set_items(self, items_data: list[tuple]):
        self.clear_list()
        for item_values in items_data:
            self.add_item(item_values)

    def on_select(self, callback):
        self.tree.bind("<<TreeviewSelect>>", lambda event: callback(self.get_selected_item()))

    def get_selected_item(self):
        selected_item = self.tree.selection()
        if selected_item:
            return self.tree.item(selected_item[0], "values")
        return None
