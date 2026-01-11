
import allure
import pytest
from api.clients.account_client import AccountClient


@pytest.mark.api
@pytest.mark.e2e
def test_account_full_lifecycle(api_request, new_user):
    """
    End-to-end test for Account: create → token → get
    (delete handled automatically in fixture)
    """
    client = AccountClient(api_request)

    username = new_user["username"]
    password = new_user["password"]
    user_id = new_user["user_id"]
    with allure.step(f"🚀 Create user: {username}"):

        allure.attach(username, name="Username",
                      attachment_type=allure.attachment_type.TEXT)
    print(f"🚀 Testing with username: {username}")

    # Generate token
    with allure.step("🔑 Generate token"):
        token_resp = client.generate_token(username, password)
        token = token_resp.json().get("token")
        allure.attach(str(token_resp.status), name="Status",
                      attachment_type=allure.attachment_type.TEXT)
        assert token is not None, "Token generation failed"

    # Get user
    with allure.step("👤 Get user details"):
        get_resp = client.get_user(user_id, token)
        allure.attach(get_resp.text(), name="Response",
                      attachment_type=allure.attachment_type.JSON)
        assert get_resp.status == 200, f"Get user failed: {get_resp.text()}"
