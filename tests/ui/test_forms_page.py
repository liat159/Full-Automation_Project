import pytest
import allure


@pytest.mark.ui
@pytest.mark.smoke
def test_textbox_form_submission(page):
    """
    Fill the Text Box form and verify submission.
    """

    page.goto("https://demoqa.com/text-box")

    with allure.step("Fill form fields"):
        page.fill("#userName", "Demo User")
        page.fill("#userEmail", "demo@example.com")
        page.fill("#currentAddress", "123 Main St")
        page.fill("#permanentAddress", "456 Side St")
        page.click("#submit")

    with allure.step("Verify submitted data"):
        output = page.locator("#output").inner_text()
        allure.attach(output, name="Form Output",
                      attachment_type=allure.attachment_type.TEXT)
        assert "Demo User" in output
        assert "demo@example.com" in output
