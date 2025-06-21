from uuid import UUID

from core.api_client import APIClient


class UserAccountsAPIClient(APIClient):

    def get_all_users_accounts(self):
        return self._make_request("GET", "/users_accounts/all")

    def get_users_accounts_by_id(self, users_accounts_id: UUID):
        return self._make_request("GET", f"/users_accounts/{users_accounts_id}")

    def create_user_accounts(self, user_id: UUID, account_id: UUID):
        return self._make_request("POST", f"/users_accounts/users/{user_id}/accounts/{account_id}")

    def delete_users_accounts(self, user_id: UUID, account_id: UUID):
        return self._make_request("DELETE", f"/users_accounts/users/{user_id}/accounts/{account_id}")


users_accounts_api_client = UserAccountsAPIClient()
