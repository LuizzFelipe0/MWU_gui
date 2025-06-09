import tkinter as tk

from MWU_gui.pages.home import HomePage
from MWU_gui.pages.user.user_page import UserPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Money With You - GUI")
        self.geometry("1024x768")

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        self._create_pages()

        self.show_page("HomePage")

    def _create_pages(self):
        home_page = HomePage(self.container, self)
        self.pages["HomePage"] = home_page
        home_page.grid(row=0, column=0, sticky="nsew")

        user_list_page = UserPage(self.container, self)
        self.pages["UserPage"] = user_list_page
        user_list_page.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page_name):
        for page in self.pages.values():
            page.hide()

        page = self.pages[page_name]
        page.show()
        page.refresh()


if __name__ == "__main__":
    app = App()
    app.mainloop()
