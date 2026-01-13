# Automation Project: DemoQA UI & API

This project demonstrates robust automation for both UI and API testing of the https://demoqa.com/ platform, including interaction with the API documentation page (Swagger).

## Tech Stack
- **Python 3.10+**
- **pytest** for running and structuring tests
- **playwright** for advanced browser automation (UI tests)
- **requests** for API interactions
- **allure-pytest** for beautiful test report generation

## Project Structure
```
DemoQA UI Automation Suite
directory: tests/ui/
Framework: Pytest + Playwright + Allure
Fixtures: ui_page_with_context, new_user
Reporting: Allure

Structure

tests/ui/
│
├── test_buttons_page.py        # Buttons: double, right, single click
├── test_alerts_page.py         # Alerts, Confirm, Prompt dialogs
├── test_frames_page.py         # Frames content verification
├── test_forms_page.py          # Text Box form submission
├── test_tables_page.py         # Add/Edit/Delete records in Web Tables
├── test_widgets_page.py        # Widgets, e.g., Date Picker

🧪 Fixtures
Fixture	Scope	Purpose
ui_page	function	Page object for basic UI test
ui_context	function	Fresh browser context for isolation
ui_page_with_context	function	Page inside fresh context, recommended for all UI tests
new_user	function	Creates a new DemoQA user for tests, cleans up after test

Test Coverage per File
1️⃣ test_buttons_page.py

Double click button

Right click button

Single click button

Allure steps + attachments of messages

2️⃣ test_alerts_page.py

Simple Alert

Confirm dialog

Prompt dialog with input

Allure steps + attachment of dialog messages

3️⃣ test_frames_page.py

Verify headings inside frame1

Verify headings inside frame2

Allure steps + attachments

4️⃣ test_forms_page.py

Fill Text Box form

Verify output section contains correct data

Allure steps + attachments

5️⃣ test_tables_page.py

Add record

Edit record (age field)

Delete record

Allure steps + attachments of table content before/after actions

6️⃣ test_widgets_page.py

Date Picker selection

Verify selected date

Allure steps + attachments

🚀 Running the Suite
Run all UI tests:
pytest -s --alluredir=allure-results tests/ui/

Run a single test file:
pytest -s --alluredir=allure-results tests/ui/test_buttons_page.py

View Allure report:
allure serve allure-results

DemoQA API Automation Suite

מיקום: tests/account/, tests/bookstore/
Framework: Pytest + Playwright (APIRequestContext) + Allure
Fixtures: api_request, new_user, book_client
Reporting: Allure

📁 Structure
tests/
│
├── account/
│   ├── test_account.py        # Full lifecycle: create → token → get → delete
│
├── bookstore/
│   ├── test_bookstore_api.py  # Add, get, update, delete books


🧪 Fixtures
Fixture	Scope	Purpose
api_request	session	Shared APIRequestContext for all API tests
new_user	function	Creates a new user, auto cleanup after test
book_client	function	API client for BookStore endpoints
🔹 Test Coverage per File
1️⃣ test_account.py
Create user (dynamic username)

Generate token

Get user details

Delete user

Allure steps + attachments of responses

2️⃣ test_bookstore_api.py

Add book (POST)

Get book details (GET)

Update book (PUT)

Delete book (DELETE)

Allure steps + attachments for each request/response

🚀 Running the API Suite
Run all API tests:
pytest -s --alluredir=allure-results tests/account/ tests/bookstore/
Run a single API test file:
pytest -s --alluredir=allure-results tests/account/test_account.py
View Allure report:
allure serve allure-results

QA Automation: Liat Karavani