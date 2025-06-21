import tkinter as tk
from tkinter import ttk
from datetime import datetime


class BaseLayout:
    def __init__(self, root):
        self.root = root
        self._setup_base_layout_style()

        self.main_container = tk.Frame(root, bg="#A0A0A0")
        self.main_container.pack(fill=tk.BOTH, expand=True)

        self.header_frame = tk.Frame(self.main_container, bg="#A0A0A0", height=60)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)

        self.content_frame = tk.Frame(self.main_container, bg="#A0A0A0")
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        self.footer_frame = tk.Frame(self.main_container, bg="#A0A0A0", height=60)
        self.footer_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self._setup_header()
        self._setup_footer()

    def _setup_base_layout_style(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure(".", font=("SF Pro Text", 12))
        style.configure("TFrame", background="#A0A0A0")
        style.configure("Header.TLabel",
                        font=("SF Pro Display", 18, "bold"),
                        background="#A0A0A0",
                        foreground="#000000")
        style.configure("Footer.TLabel",
                        font=("SF Pro Text", 12),
                        background="#A0A0A0",
                        foreground="#000000")

    def _setup_header(self):
        self.header_title = ttk.Label(
            self.header_frame,
            text="MWU - Money With You",
            style="Header.TLabel",
            font=("SF Pro Display", 18, "bold")
        )
        self.header_title.pack(side=tk.LEFT, pady=16, padx=6)

    def _setup_footer(self):
        footer_container = tk.Frame(self.footer_frame, bg="#A0A0A0")
        footer_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        copyright_frame = tk.Frame(footer_container, bg="#A0A0A0")
        copyright_frame.pack(expand=True, pady=5)

        copyright_label = ttk.Label(
            copyright_frame,
            text=f"© {datetime.now().year} Luiz Felipe",
            style="Footer.TLabel"
        )
        copyright_label.pack()

        contact_frame = tk.Frame(footer_container, bg="#A0A0A0")
        contact_frame.pack(expand=True, pady=5)

        email_label = ttk.Label(
            contact_frame,
            text="Email: lfcanariocosta04@gmail.com",
            style="FooterLink.TLabel",
            cursor="hand2"
        )
        email_label.pack()
        email_label.bind("<Button-1>", lambda e: self._open_mail())

        github_label = ttk.Label(
            contact_frame,
            text="GitHub: github.com/LuizzFelipe0",
            style="FooterLink.TLabel",
            cursor="hand2"
        )
        github_label.pack(pady=(5, 0))
        github_label.bind("<Button-1>", lambda e: self._open_github())

    def _open_mail(self):
        import webbrowser
        webbrowser.open("mailto:lfcanariocosta04@gmail.com")

    def _open_github(self):
        import webbrowser
        webbrowser.open("https://github.com/LuizzFelipe0")

    def get_content_frame(self):
        return self.content_frame