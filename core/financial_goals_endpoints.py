from uuid import UUID

from ..core.api_client import APIClient


class FinancialGoalsAPIClient(APIClient):

    def get_all_financial_goals(self):
        return self._make_request("GET", "/financial_goals/all")

    def get_financial_goals_by_id(self, financial_goals_id: UUID):
        return self._make_request("GET", f"/financial_goals/{financial_goals_id}")

    def create_financial_goals(self, financial_goals_data: dict):
        return self._make_request("POST", "/financial_goals/create", json=financial_goals_data)

    def update_financial_goals(self, financial_goals_id: UUID, financial_goals_data: dict):
        return self._make_request("PATCH", f"/financial_goals/{financial_goals_id}/update", json=financial_goals_data)

    def delete_financial_goals(self, financial_goals_id: UUID):
        return self._make_request("DELETE", f"/financial_goals/{financial_goals_id}/delete")


financial_goals_api_client = FinancialGoalsAPIClient()
