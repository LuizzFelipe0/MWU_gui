from uuid import UUID

from ..core.api_client import APIClient


class CategoryTypesAPIClient(APIClient):

    def get_all_category_types(self):
        return self._make_request("GET", "/category_types/all")

    def get_category_type_by_id(self, category_type_id: UUID):
        return self._make_request("GET", f"/category_types/{category_type_id}")

    def create_category_type(self, category_type_data: dict):
        return self._make_request("POST", "/category_types/create", json=category_type_data)

    def update_category_type(self, category_type_id: UUID, category_type_data: dict):
        return self._make_request("PATCH", f"/category_types/{category_type_id}/update", json=category_type_data)

    def delete_category_type(self, category_type_id: UUID):
        return self._make_request("DELETE", f"/category_types/{category_type_id}/delete")


category_type_api_client = CategoryTypesAPIClient()
