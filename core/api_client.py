import json
import os

import requests
from dotenv import load_dotenv
from requests import RequestException

load_dotenv()

BASE_API_URL = os.getenv("BASE_API_URL")


class APIClient:
    def __init__(self):
        self.base_url = BASE_API_URL

    def _make_request(self, method, endpoint, data=None, params=None):
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}

        try:
            if method == "GET":
                response = requests.get(url, params=params, headers=headers)
            elif method == "POST":
                response = requests.post(url, json=data, headers=headers)
            elif method == "PATCH":
                response = requests.patch(url, json=data, headers=headers)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()

            if response.status_code == 204:
                return {}

            if response.text:
                return response.json()
            else:
                return {}

        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse API response as JSON: {e}. Response: {response.text}") from e
        except RequestException as e:
            print(f"Network or API Request Error for {method} {url}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    if 'message' in error_data:
                        raise Exception(f"API Error: {error_data['message']}") from e
                except json.JSONDecodeError:
                    raise Exception(f"API Error: {e.response.text}") from e
            raise Exception(f"API request failed: {e}") from e
        except Exception as e:
            print(f"An unexpected error occurred during API request: {e}")
            raise


api_client = APIClient()
