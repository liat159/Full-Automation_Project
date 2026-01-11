import pytest
import allure


@pytest.mark.api
@pytest.mark.e2e
def test_bookstore_full_lifecycle(bookstore_client):
    client, new_user = bookstore_client
    user_id = new_user["user_id"]
    username = new_user["username"]
    password = new_user["password"]
    isbn = "9781449325862"  # דוגמה מספר ספר מהסוואגר

    with allure.step(f"👤 Testing BookStore for user: {username}"):
        allure.attach(username, name="Username",
                      attachment_type=allure.attachment_type.TEXT)
    # Generate token
    with allure.step("🔑 Generate token for new user"):
        token_resp = client.api.post(
            "/Account/v1/GenerateToken",
            data={"userName": username, "password": password}
        )
    token = token_resp.json().get("token")
    assert token, "Token generation failed"

    with allure.step("➕ Add book to collection"):
        create_resp = client.create_book(user_id, isbn, token=token)
        assert create_resp.status in (
            200, 201), f"Failed to add book: {create_resp.text()}"
        allure.attach(create_resp.text(), name="Create Response",
                      attachment_type=allure.attachment_type.JSON)

    with allure.step("📖 Get user books"):
        get_resp = client.get_books(user_id=user_id, token=token)
        assert get_resp.status == 200
        allure.attach(get_resp.text(), name="Books Response",
                      attachment_type=allure.attachment_type.JSON)

    with allure.step("🗑️ Delete book from collection"):
        del_resp = client.delete_book(user_id, isbn, token=token)
        assert del_resp.status == 204
        allure.attach(del_resp.text(), name="Delete Response",
                      attachment_type=allure.attachment_type.JSON)
