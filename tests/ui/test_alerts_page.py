import pytest
import allure


@pytest.mark.ui
@pytest.mark.smoke
def test_alerts_handling(ui_page_with_context):
    """
    Tests Alerts, Confirm, Prompt dialogs in DemoQA Alerts page.
    """
    page = ui_page_with_context

    with allure.step("Navigate to Alerts page"):
        page.goto("https://demoqa.com/alerts")
        assert page.get_by_role('heading', name='Alerts', level=1).is_visible()

    # ---------- Simple Alert ----------
    with allure.step("Click button for alert and accept it"):
        with page.expect_event("dialog") as dialog_info:
            page.locator('#alertButton').click(force=True)

    dialog = dialog_info.value
    alert_text = dialog.message
    dialog.accept()

    allure.attach(
        alert_text,
        name="Alert Text",
        attachment_type=allure.attachment_type.TEXT
    )

    assert "You clicked a button" in alert_text

    # ---------- Confirm Alert ----------
    with allure.step("Click confirm button and accept"):
        with page.expect_event("dialog") as dialog_info:
            page.evaluate("document.getElementById('confirmButton').click()")

        dialog = dialog_info.value
        confirm_text = dialog.message
        dialog.accept()

        allure.attach(
            confirm_text,
            name="Confirm Alert Text",
            attachment_type=allure.attachment_type.TEXT
        )
    assert "You clicked Ok" in confirm_text or "You selected Ok" in confirm_text

    # ---------- Prompt Alert ----------
    with allure.step("Click prompt button and send keys"):
        prompt_input = "DemoUser"

    with page.expect_event("dialog") as dialog_info:
        page.evaluate("document.getElementById('promtButton').click()")

        dialog = dialog_info.value
        prompt_text = dialog.message
        dialog.accept(prompt_input)

        allure.attach(
            prompt_text,
            name="Prompt Alert Text",
            attachment_type=allure.attachment_type.TEXT
        )

    assert "Please enter your name" in prompt_text
