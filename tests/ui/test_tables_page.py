import pytest
import allure


@pytest.mark.ui
@pytest.mark.smoke
def test_web_tables(page):
    """
    Verify Web Tables interactions: add, edit, delete records.
    """

    page.goto("https://demoqa.com/webtables")

    # ---------- Add Record ----------
    with allure.step("Add a new record"):
        page.click("#addNewRecordButton")
        page.fill("#firstName", "Demo")
        page.fill("#lastName", "User")
        page.fill("#userEmail", "demo@example.com")
        page.fill("#age", "30")
        page.fill("#salary", "5000")
        page.fill("#department", "QA")
        page.click("#submit")

    # ---------- Verify Record ----------
    with allure.step("Verify new record exists in the table"):
        table_text = page.locator(".rt-tbody").inner_text()
        allure.attach(table_text, name="Table Content",
                      attachment_type=allure.attachment_type.TEXT)
        assert "Demo" in table_text
        assert "User" in table_text
        assert "demo@example.com" in table_text

    # ---------- Edit Record ----------
    with allure.step("Edit the record age to 35"):
        page.click("span[title='Edit']")  # assumes first row edit
        page.fill("#age", "35")
        page.click("#submit")
        updated_text = page.locator(".rt-tbody").inner_text()
        allure.attach(updated_text, name="Updated Table Content",
                      attachment_type=allure.attachment_type.TEXT)
        assert "35" in updated_text

    # ---------- Delete Record ----------
    with allure.step("Delete the record"):
        page.click("span[title='Delete']")  # assumes first row delete
        deleted_text = page.locator(".rt-tbody").inner_text()
        allure.attach(deleted_text, name="Table After Deletion",
                      attachment_type=allure.attachment_type.TEXT)
        assert "Demo" in deleted_text
