import pytest
import allure


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.priority_Medium
def test_datepicker_widget(ui_page_with_context):
    """
    Verify Date Picker widget on DemoQA Widgets page.
    """
    page = ui_page_with_context
    page.goto("https://demoqa.com/date-picker")

    with allure.step("Select date"):
        date_input = page.locator("#datePickerMonthYearInput")
        date_input.click()
        date_input.fill("01/08/2026")
        date_input.press("Enter")

    with allure.step("Verify selected date"):
        selected_date = page.locator("#datePickerMonthYearInput").input_value()
        allure.attach(selected_date, name="Selected Date",
                      attachment_type=allure.attachment_type.TEXT)
        assert selected_date == "01/08/2026"
