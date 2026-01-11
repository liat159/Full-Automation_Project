import pytest
import allure
from api.clients.account_client import AccountClient


@pytest.mark.ui
@pytest.mark.e2e
def test_bookstore_ui_flow(ui_page_with_context, new_user):
    """
    Full end-to-end UI test for BookStore:
    1️⃣ Login
    2️⃣ Add book to collection
    3️⃣ Verify book is in collection
    4️⃣ Delete book from collection
    """

    page = ui_page_with_context
    username = new_user["username"]
    password = new_user["password"]
    user_id = new_user["user_id"]

    isbn = "9781449325862"  # ספר לדוגמה מהסוואגר

    # ----------------- LOGIN -----------------
    with allure.step("🔹 Navigate to login page"):
        page.goto("https://demoqa.com/login")
        assert page.locator("text=Login").is_visible(
        ), "Login page title not visible"

    with allure.step(f"🔹 Fill login form for user: {username}"):
        page.fill("#userName", username)
        page.fill("#password", password)
        page.click("#login")

    with allure.step("🔹 Verify successful login"):
        assert page.locator("#submit").is_visible() or page.locator(
            "text=Log out").is_visible(), "Login failed"
        allure.attach(page.url, name="Current URL after login",
                      attachment_type=allure.attachment_type.TEXT)

    # ----------------- ADD BOOK -----------------
    with allure.step(f"➕ Add book with ISBN: {isbn}"):
        page.goto("https://demoqa.com/books")
        page.click(f"text={isbn}")  # בוחר את הספר
        page.click("text=Add To Your Collection")
        # אפשר לבדוק את alert
        if page.locator(".modal-body").is_visible():
            msg = page.locator(".modal-body").inner_text()
            allure.attach(msg, name="Add Book Message",
                          attachment_type=allure.attachment_type.TEXT)
            page.click("button#closeSmallModal")  # סוגר modal

    # ----------------- VERIFY BOOK -----------------
    with allure.step("📖 Verify book appears in user collection"):
        page.goto("https://demoqa.com/profile")
        assert page.locator(f"text={isbn}").is_visible(
        ), f"Book {isbn} not found in collection"
        allure.attach(page.inner_text("div#userBooks"), name="Books Collection",
                      attachment_type=allure.attachment_type.TEXT)

    # ----------------- DELETE BOOK -----------------
    with allure.step("🗑️ Delete book from collection"):
        page.click(f"text={isbn}")  # בוחר את הספר
        page.click("text=Delete")
        # Modal confirmation
        if page.locator("#closeSmallModal").is_visible():
            page.click("#closeSmallModal")
        assert not page.locator(f"text={isbn}").is_visible(
        ), "Book still present after deletion"
