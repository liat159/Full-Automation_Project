import pytest
import allure


@pytest.mark.ui
@pytest.mark.smoke
def test_demoqa_login(page):
    """
    Basic UI test: login page loads and login fails with invalid credentials.
    """

    with allure.step("🔹 Navigate to login page"):
        page.goto("https://demoqa.com/login")
        assert page.get_by_role(
            "heading", name="Login", exact=True
        ).is_visible(), "Login heading not visible"

    with allure.step("🔹 Fill username and password"):
        page.fill("#userName", "liat85.hason@gmail.com")
        page.fill("#password", "Votiro#lavi2019")

    with allure.step("🔹 Click login button"):
        page.get_by_role('button', name='Login').click()

    with allure.step("🔹 Verify successful login"):
        page.wait_for_url("**/profile")

        allure.attach(
            page.url,
            name="Current URL after login",
            attachment_type=allure.attachment_type.TEXT
        )
