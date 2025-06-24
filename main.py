import tkinter as tk

from components.base_layout_component import BaseLayout
from pages.accounts.account_create_page import AccountCreatePage
from pages.accounts.account_page import AccountsPage
from pages.accounts.account_update_page import AccountUpdatePage
from pages.categories.category_create_page import CategoryCreatePage
from pages.categories.category_page import CategoryPage
from pages.categories.category_update_page import CategoryUpdatePage
from pages.category_types.category_types_create_page import CategoryTypeCreatePage
from pages.category_types.category_types_page import CategoryTypesPage
from pages.category_types.category_types_update_page import CategoryTypeUpdatePage
from pages.financial_goals.financial_goals_create_page import FinancialGoalsCreatePage
from pages.financial_goals.financial_goals_page import FinancialGoalsPage
from pages.financial_goals.financial_goals_update_page import FinancialGoalsUpdatePage
from pages.home import HomePage
from pages.transactions.transaction_create_page import TransactionCreatePage
from pages.transactions.transaction_page import TransactionPage
from pages.transactions.transaction_update_page import TransactionUpdatePage
from pages.user.user_create_page import UserCreatePage
from pages.user.user_page import UserPage
from pages.user.user_update_page import UserUpdatePage
from pages.user_accounts.user_accounts_create_page import UserAccountsCreatePage
from pages.user_accounts.user_accounts_page import UserAccountsPage
from pages.user_accounts.user_accounts_update_page import UserAccountsUpdatePage


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Money With You - GUI")

        self.ios_layout = BaseLayout(self)

        self.container = self.ios_layout.get_content_frame()
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {}
        self._create_pages()

        self.show_page("HomePage")


    def _create_pages(self):
        home_page = HomePage(self.container, self)
        self.pages["HomePage"] = home_page
        home_page.grid(row=0, column=0, sticky="nsew")

        account_list_page = AccountsPage(self.container, self)
        self.pages["AccountsPage"] = account_list_page
        account_list_page.grid(row=0, column=0, sticky="nsew")

        account_update_page = AccountUpdatePage(self.container, self)
        self.pages["AccountUpdatePage"] = account_update_page
        account_update_page.grid(row=0, column=0, sticky="nsew")

        account_create_page = AccountCreatePage(self.container, self)
        self.pages["AccountCreatePage"] = account_create_page
        account_create_page.grid(row=0, column=0, sticky="nsew")

        category_list_page = CategoryPage(self.container, self)
        self.pages["CategoryPage"] = category_list_page
        category_list_page.grid(row=0, column=0, sticky="nsew")
        
        category_update_page = CategoryUpdatePage(self.container, self)
        self.pages["CategoryUpdatePage"] = category_update_page
        category_update_page.grid(row=0, column=0, sticky="nsew")

        category_create_page = CategoryCreatePage(self.container, self)
        self.pages["CategoryCreatePage"] = category_create_page
        category_create_page.grid(row=0, column=0, sticky="nsew")

        category_type_list_page = CategoryTypesPage(self.container, self)
        self.pages["CategoryTypesPage"] = category_type_list_page
        category_type_list_page.grid(row=0, column=0, sticky="nsew")

        category_type_update_page = CategoryTypeUpdatePage(self.container, self)
        self.pages["CategoryTypeUpdatePage"] = category_type_update_page
        category_type_update_page.grid(row=0, column=0, sticky="nsew")

        category_type_create_page = CategoryTypeCreatePage(self.container, self)
        self.pages["CategoryTypeCreatePage"] = category_type_create_page
        category_type_create_page.grid(row=0, column=0, sticky="nsew")
        
        financial_goals_list_page = FinancialGoalsPage(self.container, self)
        self.pages["FinancialGoalsPage"] = financial_goals_list_page
        financial_goals_list_page.grid(row=0, column=0, sticky="nsew")

        financial_goals_update_page = FinancialGoalsUpdatePage(self.container, self)
        self.pages["FinancialGoalsUpdatePage"] = financial_goals_update_page
        financial_goals_update_page.grid(row=0, column=0, sticky="nsew")

        financial_goals_create_page = FinancialGoalsCreatePage(self.container, self)
        self.pages["FinancialGoalsCreatePage"] = financial_goals_create_page
        financial_goals_create_page.grid(row=0, column=0, sticky="nsew")

        user_accounts_list_page = UserAccountsPage(self.container, self)
        self.pages["UserAccountsPage"] = user_accounts_list_page
        user_accounts_list_page.grid(row=0, column=0, sticky="nsew")

        user_accounts_update_page = UserAccountsUpdatePage(self.container, self)
        self.pages["UserAccountsUpdatePage"] = user_accounts_update_page
        user_accounts_update_page.grid(row=0, column=0, sticky="nsew")

        user_accounts_create_page = UserAccountsCreatePage(self.container, self)
        self.pages["UserAccountsCreatePage"] = user_accounts_create_page
        user_accounts_create_page.grid(row=0, column=0, sticky="nsew")
        
        transaction_list_page = TransactionPage(self.container, self)
        self.pages["TransactionPage"] = transaction_list_page
        transaction_list_page.grid(row=0, column=0, sticky="nsew")

        transaction_update_page = TransactionUpdatePage(self.container, self)
        self.pages["TransactionUpdatePage"] = transaction_update_page
        transaction_update_page.grid(row=0, column=0, sticky="nsew")

        transaction_create_page = TransactionCreatePage(self.container, self)
        self.pages["TransactionCreatePage"] = transaction_create_page
        transaction_create_page.grid(row=0, column=0, sticky="nsew")

        user_list_page = UserPage(self.container, self)
        self.pages["UserPage"] = user_list_page
        user_list_page.grid(row=0, column=0, sticky="nsew")

        user_update_page = UserUpdatePage(self.container, self)
        self.pages["UserUpdatePage"] = user_update_page
        user_update_page.grid(row=0, column=0, sticky="nsew")

        user_create_page = UserCreatePage(self.container, self)
        self.pages["UserCreatePage"] = user_create_page
        user_create_page.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page_name, **kwargs):
        for page in self.pages.values():
            page.hide()

        page = self.pages[page_name]
        page.show()
        page.refresh(**kwargs)


if __name__ == "__main__":
    app = App()
    app.mainloop()
