from uuid import UUID

from ..core.api_client import APIClient


class UserAPIClient(APIClient):

    def get_all_users(self):
        return self._make_request("GET", "/users/all")

    def get_deleted_users(self):
        return self._make_request("GET", "/users/deleted")

    def get_user_by_id(self, user_id: UUID):
        return self._make_request("GET", f"/users/{user_id}")

    def create_user(self, user_data: dict):
        # O FastAPI espera o body como JSON
        return self._make_request("POST", "/users/create", json=user_data)

    def update_user(self, user_id: UUID, user_data: dict):
        return self._make_request("PATCH", f"/users/{user_id}/update", json=user_data)

    def delete_user(self, user_id: UUID):
        return self._make_request("DELETE", f"/users/{user_id}/delete")

    def restore_user(self, user_id: UUID):
        return self._make_request("POST", f"/users/{user_id}/restore")

    def force_delete_user(self, user_id: UUID):
        return self._make_request("DELETE", f"/users/{user_id}/force-delete")


user_api_client = UserAPIClient()
