from uuid import UUID

from ..core.api_client import APIClient


class UsersEndpoints(APIClient):

    def get_all_users(self):
        return self._make_request("GET", "/users/all")

    def get_user_by_id(self, user_id: UUID):
        return self._make_request("GET", f"/users/{user_id}")


users_api = UsersEndpoints()
