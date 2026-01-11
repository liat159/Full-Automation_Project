import json
import uuid
import time
from playwright.sync_api import APIRequestContext


class AccountClient:
    def __init__(self, api_request: APIRequestContext):
        self.api = api_request

    def create_user(self, username: str = None, password: str = None):
        """
        Creates a user. If username or password not provided, generates them dynamically.
        Returns APIResponse or None if request fails.
        """
        if username is None:
            username = f"user_{uuid.uuid4().hex[:8]}"
        if password is None:
            password = "Password123!"

        data = {"userName": username, "password": password}
        print("🚀 SENDING USERNAME:", data["userName"])

        try:
            resp = self.api.post("/Account/v1/User", data=json.dumps(data))
            if resp is None:
                print("⚠️ API returned None!")
                return None
            return resp
        except Exception as e:
            print("⚠️ Exception in create_user:", e)
            return None

    def generate_token(self, username: str, password: str):
        payload = {"userName": username, "password": password}
        return self.api.post("/Account/v1/GenerateToken", data=payload)

    def authorize(self, username: str, password: str):
        payload = {"userName": username, "password": password}
        return self.api.post("/Account/v1/Authorized", data=payload)

    def get_user(self, user_id: str, token: str):
        return self.api.get(
            f"/Account/v1/User/{user_id}",
            headers={"Authorization": f"Bearer {token}"}
        )

    def delete_user(self, user_id: str, token: str):
        return self.api.delete(
            f"/Account/v1/User/{user_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
