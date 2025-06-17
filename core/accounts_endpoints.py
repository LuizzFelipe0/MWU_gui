from uuid import UUID

from ..core.api_client import APIClient


class AccountAPIClient(APIClient):

    def get_all_accounts(self):
        return self._make_request("GET", "/accounts/all")

    def get_deleted_accounts(self):
        return self._make_request("GET", "/accounts/deleted")

    def get_account_by_id(self, account_id: UUID):
        return self._make_request("GET", f"/accounts/{account_id}")

    def create_account(self, account_data: dict):
        # O FastAPI espera o body como JSON
        return self._make_request("POST", "/accounts/create", json=account_data)

    def update_account(self, account_id: UUID, account_data: dict):
        return self._make_request("PATCH", f"/accounts/{account_id}/update", json=account_data)

    def delete_account(self, account_id: UUID):
        return self._make_request("DELETE", f"/accounts/{account_id}/delete")

    def restore_account(self, account_id: UUID):
        return self._make_request("POST", f"/accounts/{account_id}/restore")

    def force_delete_account(self, account_id: UUID):
        return self._make_request("DELETE", f"/accounts/{account_id}/force-delete")


account_api_client = AccountAPIClient()
