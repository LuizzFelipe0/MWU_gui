from uuid import UUID

from core.api_client import APIClient


class AccountAPIClient(APIClient):

    def get_all_categories(self):
        return self._make_request("GET", "/categories/all")

    def get_deleted_categories(self):
        return self._make_request("GET", "/categories/deleted")

    def get_category_by_id(self, category_id: UUID):
        return self._make_request("GET", f"/categories/{category_id}")

    def create_category(self, category_data: dict):
        return self._make_request("POST", "/categories/create", json=category_data)

    def update_category(self, category_id: UUID, category_data: dict):
        return self._make_request("PATCH", f"/categories/{category_id}/update", json=category_data)

    def delete_category(self, category_id: UUID):
        return self._make_request("DELETE", f"/categories/{category_id}/delete")

    def restore_category(self, category_id: UUID):
        return self._make_request("POST", f"/categories/{category_id}/restore")

    def force_delete_category(self, category_id: UUID):
        return self._make_request("DELETE", f"/categories/{category_id}/force-delete")


category_api_client = AccountAPIClient()
