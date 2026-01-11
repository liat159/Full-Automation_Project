import pytest
import allure

BOOKS = [
    {"isbn": "9781449337711", "title": "Designing Evolvable Web APIs"},
    {"isbn": "9781449325862", "title": "Git Pocket Guide"},
    {"isbn": "9781449331818", "title": "Learning JS Design Patterns"}
]


@pytest.fixture(scope="session")
def ui_user():
    """
     Stable user for UI login tests (DemoQA limitation)
     """
    return {
        "username": "liat85.hason@gmail.com",
        "password": "Votiro#lavi2019"
    }


@pytest.mark.ui
@pytest.mark.regression
class TestBookStoreAdvanced:

    @pytest.mark.e2e
    def test_add_multiple_books(self, ui_page_with_context, ui_user):
        """
        Add multiple books to a new user's collection and verify them.
        """
        page = ui_page_with_context
        username = ui_user["username"]
        password = ui_user["password"]

        # -------- LOGIN --------
        with allure.step(f"Login as user {username}"):
            page.goto("https://demoqa.com/login")
            page.fill("#userName", username)
            page.fill("#password", password)
            page.click("#login")
            page.wait_for_url("**/profile")

        # -------- ADD BOOKS --------
        for book in BOOKS:
            with allure.step(f"Add book {book['title']} ({book['isbn']})"):
                page.goto("https://demoqa.com/books")
                page.click(f"text={book['isbn']}")
                page.click("text=Add To Your Collection")
                if page.locator(".modal-body").is_visible():
                    msg = page.locator(".modal-body").inner_text()
                    allure.attach(
                        msg, name=f"Add Book Message {book['isbn']}", attachment_type=allure.attachment_type.TEXT)
                    page.click("button#closeSmallModal")

        # -------- VERIFY BOOKS --------
        with allure.step("Verify all books in collection"):
            page.goto("https://demoqa.com/profile")
            for book in BOOKS:
                assert page.locator(f"text={book['isbn']}").is_visible(
                ), f"Book {book['title']} not found"
            allure.attach(page.inner_text("div#userBooks"), name="Books Collection",
                          attachment_type=allure.attachment_type.TEXT)

        # -------- DELETE BOOKS --------
        for book in BOOKS:
            with allure.step(f"Delete book {book['title']} ({book['isbn']})"):
                page.click(f"text={book['isbn']}")
                page.click("text=Delete")
                if page.locator("#closeSmallModal").is_visible():
                    page.click("#closeSmallModal")
                assert not page.locator(f"text={book['isbn']}").is_visible(
                ), f"Book {book['title']} still present after deletion"
