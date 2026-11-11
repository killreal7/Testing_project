from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
import requests
from src.main.api.config.config import Config


class RequestsSpecs:
    @staticmethod
    def base_headers():
        return {
            "Content-Type": "application/json",
            "accept": "application/json"
        }

    @staticmethod
    def auth_headers(username: str, password: str):
        base_url = Config.fetch("BackendUrl")
        request = LoginUserRequest(username=username, password=password)
        response = requests.post(
            url=f"{base_url}/auth/token/login",
            json=request.model_dump(),
            headers=RequestsSpecs.base_headers()
        )
        if response.status_code == 200:
            response_data = LoginUserResponse(**response.json())
            token = response_data.token
            headers = RequestsSpecs.base_headers()
            headers["Authorization"] = f"Bearer {token}"
            return headers
        else:
            raise Exception(f"Failed to login. Status: {response.status_code}, Response: {response.text}")

    @staticmethod
    def unauth_headers():
        return RequestsSpecs.base_headers()