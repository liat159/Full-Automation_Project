import pytest
import allure


@pytest.mark.ui
@pytest.mark.smoke
def test_buttons_interactions(ui_page_with_context):
    """
    Tests multiple button interactions on DemoQA Buttons page:
    - doubleClick
    - rightClick
    - click
    """

    page = ui_page_with_context

    with allure.step("Navigate to Buttons page"):
        page.goto("https://demoqa.com/buttons")
        assert page.get_by_role(
            'heading', name='Buttons', level=1).is_visible()

    with allure.step("Double click on button"):
        dc_btn = page.locator("#doubleClickBtn")
        dc_btn.dblclick()
        msg = page.locator("#doubleClickMessage").inner_text()
        allure.attach(msg, name="Double Click Message",
                      attachment_type=allure.attachment_type.TEXT)
        assert "You have done a double click" in msg

    with allure.step("Right click on button"):
        rc_btn = page.locator("#rightClickBtn")
        rc_btn.click(button="right")
        msg = page.locator("#rightClickMessage").inner_text()
        allure.attach(msg, name="Right Click Message",
                      attachment_type=allure.attachment_type.TEXT)
        assert "You have done a right click" in msg

    with allure.step("Single click on dynamic click button"):

        page.locator('#QvYkw').click()
        msg = page.locator('//p[@id="dynamicClickMessage"]').inner_text()
        allure.attach(msg, name="Click Message",
                      attachment_type=allure.attachment_type.TEXT)
        assert "You have done a dynamic click" in msg
