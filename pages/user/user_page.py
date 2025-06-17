import tkinter as tk
from datetime import datetime  # Importar para formatar datetimes para exibição
from tkinter import ttk, messagebox
from uuid import UUID

from MWU_gui.components.list_box_component import ListBoxComponent
from MWU_gui.core.users_endpoints import user_api_client  # Certifique-se de que é 'user_api_client'
from MWU_gui.pages.base_page import BasePage


class UserPage(BasePage):
    def __init__(self, parent, controller=None, *args, **kwargs):
        super().__init__(parent, controller, *args, **kwargs)
        self.user_data = []  # Para armazenar os dados brutos da API

    def _setup_ui(self):
        # Configuração do grid principal da página
        self.grid_rowconfigure(0, weight=0)  # Linha para título e botão "Create"
        self.grid_rowconfigure(1, weight=1)  # Linha para a ListBoxComponent (expande)
        self.grid_rowconfigure(2, weight=0)  # Linha para o botão "Refresh"

        self.grid_columnconfigure(0, weight=1)  # Coluna para conteúdo principal (expande)
        self.grid_columnconfigure(1, weight=0)  # Coluna para o botão "Create User" (não expande)

        # --- Botão "Back to Home" (Canto Superior Esquerdo) ---
        if self.controller:
            home_button = ttk.Button(self, text="< Back to Home",
                                     command=lambda: self.controller.show_page("HomePage"))
            home_button.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        else:
            print("Warning: Controller not provided to UserPage. 'Back to Home' button disabled.")

        # --- Título da Página "Users" ---
        title_label = tk.Label(self, text="Users", font=("Arial", 20, "bold"), pady=10)
        title_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")  # Centralizado acima do conteúdo

        # --- Botão "Create New User" (Canto Superior Direito) ---
        create_user_button = ttk.Button(self, text="Create New User",
                                        command=lambda: self.controller.show_page("UserCreatePage"))
        # Posicionamento no canto superior direito
        create_user_button.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

        # --- Configuração das Colunas e Cabeçalhos para o ListBoxComponent ---
        self.columns = ["id", "first_name", "last_name", "cpf", "email",
                        "manual_balance", "created_at", "updated_at", "deleted_at"]  # Incluindo todos os campos

        self.display_headings = {
            "id": "ID",
            "first_name": "First Name",
            "last_name": "Last Name",
            "cpf": "CPF",
            "email": "Email",
            "manual_balance": "Balance",
            "created_at": "Created At",
            "updated_at": "Updated At",
            "deleted_at": "Deleted At"
        }

        self.user_list_component = ListBoxComponent(self, columns=self.columns, display_headings=self.display_headings)
        self.user_list_component.grid(row=1, column=0, columnspan=2, padx=10, pady=10,
                                      sticky="nsew")  # Ocupa a linha do meio
        self.user_list_component.on_select(self._on_user_selected)  # Bind de seleção

        # --- Botão "Refresh Users" ---
        refresh_button = ttk.Button(self, text="Refresh Users", command=self._load_users)
        refresh_button.grid(row=2, column=0, columnspan=2, pady=5)  # Na parte inferior

        # Carrega os usuários na inicialização da UI
        self._load_users()

    def _load_users(self):
        try:
            users_raw_data = user_api_client.get_all_users()  # Use user_api_client aqui
            self.user_data = users_raw_data  # Armazena os dados brutos
            items_for_list = []
            for user in users_raw_data:
                row_values = []
                for col in self.columns:
                    value = user.get(col, '')  # Use get com default para evitar KeyError
                    # Formatar UUID e datetime para string
                    if isinstance(value, UUID):
                        row_values.append(str(value))
                    elif isinstance(value, datetime):
                        row_values.append(value.strftime("%Y-%m-%d %H:%M:%S"))
                    else:
                        row_values.append(value)
                items_for_list.append(tuple(row_values))
            self.user_list_component.set_items(items_for_list)
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to load users: {e}")
            self.user_list_component.clear_list()

    def _on_user_selected(self, selected_values):
        """Callback quando um usuário é selecionado na lista."""
        if selected_values:
            user_id = selected_values[0]  # Assumindo que o ID é a primeira coluna
            if self.controller:
                # --- REDIRECIONAMENTO PARA A PÁGINA DE UPDATE/DETAIL ---
                self.controller.show_page("UserUpdatePage", user_id=user_id)  # Mudei para UserUpdatePage
            else:
                messagebox.showerror("Error", "Controller not available to show detail page.")
        else:
            pass  # Nenhuma seleção, pode ignorar

    def refresh(self):
        """Método de refresh chamado pelo App.show_page para recarregar os dados."""
        self._load_users()
