from playwright.sync_api import APIRequestContext
import json
print("📦 bookstore_client LOADED")


class BookStoreClient:
    print("📘 BookStoreClient class defined")

    def __init__(self, api_request: APIRequestContext):
        self.api = api_request

    # ---------------- CREATE ----------------
    def create_book(self, user_id: str, isbn: str, token: str = None):
        data = {"userId": user_id, "collectionOfIsbns": [{"isbn": isbn}]}
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        return self.api.post("/BookStore/v1/Books", data=json.dumps(data), headers=headers)

    # ---------------- GET ----------------

    def get_books(self, user_id: str, token: str = None):
        """
        Get all books of a user
        """
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        return self.api.get(f"/Account/v1/User/{user_id}", headers=headers)

    # ---------------- DELETE ----------------
    def delete_book(self, user_id: str, isbn: str, token: str = None):
        data = {"isbn": isbn, "userId": user_id}
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        return self.api.delete("/BookStore/v1/Book", data=json.dumps(data), headers=headers)
