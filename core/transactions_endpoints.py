from uuid import UUID

from core.api_client import APIClient


class TransactionAPIClient(APIClient):

    def get_all_transactions(self):
        return self._make_request("GET", "/transactions/all")

    def get_deleted_transactions(self):
        return self._make_request("GET", "/transactions/deleted")

    def get_transaction_by_id(self, transaction_id: UUID):
        return self._make_request("GET", f"/transactions/{transaction_id}")

    def create_transaction(self, transaction_data: dict):
        return self._make_request("POST", "/transactions/create", data=transaction_data)

    def update_transaction(self, transaction_id: UUID, transaction_data: dict):
        return self._make_request("PATCH", f"/transactions/{transaction_id}/update", data=transaction_data)

    def delete_transaction(self, transaction_id: UUID):
        return self._make_request("DELETE", f"/transactions/{transaction_id}/delete")

    def restore_transaction(self, transaction_id: UUID):
        return self._make_request("POST", f"/transactions/{transaction_id}/restore")

    def force_delete_transaction(self, transaction_id: UUID):
        return self._make_request("DELETE", f"/transactions/{transaction_id}/force-delete")


transaction_api_client = TransactionAPIClient()
