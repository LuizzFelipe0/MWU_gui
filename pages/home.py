import tkinter as tk
from tkinter import ttk

from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)

    def _setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Blue.TButton", background="#007AFF", foreground="white",
                        font=("Arial", 12, "bold"), borderwidth=0, relief="flat")
        style.map("Blue.TButton",
                  background=[("active", "#0056B3"), ("!disabled", "#007AFF")],
                  foreground=[("active", "white"), ("!disabled", "white")])

        style.configure("Green.TButton", background="#34C759", foreground="white",
                        font=("Arial", 12, "bold"), borderwidth=0, relief="flat")
        style.map("Green.TButton",
                  background=[("active", "#28A745"), ("!disabled", "#34C759")],
                  foreground=[("active", "white"), ("!disabled", "white")])

        style.configure("Orange.TButton", background="#FF9500", foreground="white",
                        font=("Arial", 12, "bold"), borderwidth=0, relief="flat")
        style.map("Orange.TButton",
                  background=[("active", "#CC7A00"), ("!disabled", "#FF9500")],
                  foreground=[("active", "white"), ("!disabled", "white")])

        style.configure("Purple.TButton", background="#AF52DE", foreground="white",
                        font=("Arial", 12, "bold"), borderwidth=0, relief="flat")
        style.map("Purple.TButton",
                  background=[("active", "#8C42B2"), ("!disabled", "#AF52DE")],
                  foreground=[("active", "white"), ("!disabled", "white")])

        style.configure("Red.TButton", background="#FF3B30", foreground="white",
                        font=("Arial", 12, "bold"), borderwidth=0, relief="flat")
        style.map("Red.TButton",
                  background=[("active", "#CC2D25"), ("!disabled", "#FF3B30")],
                  foreground=[("active", "white"), ("!disabled", "white")])

        style.configure("Gray.TButton", background="#8E8E93", foreground="white",
                        font=("Arial", 12, "bold"), borderwidth=0, relief="flat")
        style.map("Gray.TButton",
                  background=[("active", "#707073"), ("!disabled", "#8E8E93")],
                  foreground=[("active", "white"), ("!disabled", "white")])

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=2)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center_frame = tk.Frame(self)
        center_frame.grid(row=0, column=0, rowspan=6, sticky="nsew", padx=50, pady=50)

        center_frame.grid_rowconfigure(0, weight=0)
        center_frame.grid_rowconfigure(1, weight=0)
        center_frame.grid_rowconfigure(2, weight=1)
        center_frame.grid_rowconfigure(3, weight=0)
        center_frame.grid_rowconfigure(4, weight=1)
        center_frame.grid_columnconfigure(0, weight=1)

        title_label = tk.Label(center_frame, text="MWU Adminstration Panel",
                               font=("Arial", 24, "bold"), fg="#2C3E50")
        title_label.grid(row=0, column=0, pady=(50, 10), sticky="n")

        description_text = (
            "Your personal finance management application has finally arrived. "
            "Track expenses, categorize income, and achieve your financial goals "
            "with our app."
        )
        description_label = tk.Label(center_frame, text=description_text,
                                     font=("Arial", 12), wraplength=400, justify="center",
                                     fg="#555555")
        description_label.grid(row=1, column=0, pady=(0, 30), sticky="n")

        navigation_frame = tk.Frame(center_frame)
        navigation_frame.grid(row=3, column=0, padx=10, pady=10,
                              sticky="")

        navigation_frame.grid_columnconfigure(0, weight=1)
        navigation_frame.grid_columnconfigure(1, weight=1)
        for i in range(5):
            navigation_frame.grid_rowconfigure(i, weight=1)

        buttons_info = [
            ("Analytics", "AnalyticsPage", "Purple.TButton"),
            ("Users", "UserPage", "Blue.TButton"),
            ("Transactions", "TransactionsPage", "Green.TButton"),
            ("User Accounts", "UserAccountsPage", "Orange.TButton"),
            ("Accounts", "AccountsPage", "Purple.TButton"),
            ("Financial Goals", "FinancialGoalsPage", "Red.TButton"),
            ("Categories", "CategoryPage", "Blue.TButton"),
            ("Category Types", "CategoryTypesPage", "Green.TButton"),
        ]

        row_idx = 0
        col_idx = 0
        for text, page_name, btn_style in buttons_info:
            button = ttk.Button(navigation_frame, text=text, style=btn_style,
                                command=lambda name=page_name: self.controller.show_page(name))
            button.grid(row=row_idx, column=col_idx, padx=10, pady=10,
                        sticky="ew")
            col_idx += 1
            if col_idx > 1:
                col_idx = 0
                row_idx += 1
