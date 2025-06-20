from uuid import UUID

from ..core.api_client import APIClient


class UserAccountsAPIClient(APIClient):

    def get_all_users_accounts(self):
        return self._make_request("GET", "/users_accounts/all")

    def get_users_accounts_by_id(self, users_accounts_id: UUID):
        return self._make_request("GET", f"/users_accounts/{users_accounts_id}")

    def create_users_accounts(self, users_accounts_data: dict):
        return self._make_request("POST", "/users_accounts/create", json=users_accounts_data)

    def update_users_accounts(self, users_accounts_id: UUID, users_accounts_data: dict):
        return self._make_request("PATCH", f"/users_accounts/{users_accounts_id}/update", json=users_accounts_data)

    def delete_users_accounts(self, users_accounts_id: UUID):
        return self._make_request("DELETE", f"/users_accounts/{users_accounts_id}/delete")

    def restore_users_accounts(self, users_accounts_id: UUID):
        return self._make_request("POST", f"/users_accounts/{users_accounts_id}/restore")

    def force_delete_users_accounts(self, users_accounts_id: UUID):
        return self._make_request("DELETE", f"/users_accounts/{users_accounts_id}/force-delete")


users_accounts_api_client = UserAccountsAPIClient()
