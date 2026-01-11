from api.clients.account_client import AccountClient
import os
import sys
import time
import uuid
from typing import Generator

import pytest
from playwright.sync_api import APIRequestContext, Page, Browser, BrowserContext

# ------------------------------
# Fix Python path for imports
# ------------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# ------------------------------
# MARKERS + CONFIG
# ------------------------------


def pytest_configure(config):
    config.addinivalue_line("markers", "ui: UI tests")
    config.addinivalue_line("markers", "api: API tests")
    config.addinivalue_line("markers", "smoke: smoke tests")
    config.addinivalue_line("markers", "regression: full regression suite")
    config.addinivalue_line("markers", "e2e: end-to-end flows")
    config.addinivalue_line("markers", "negative: negative scenarios")

# ------------------------------
# API FIXTURE
# ------------------------------


@pytest.fixture(scope="session")
def api_request(playwright) -> Generator[APIRequestContext, None, None]:
    """
    Shared API request context for API tests.
    """
    context = playwright.request.new_context(
        base_url="https://demoqa.com",
        extra_http_headers={"Content-Type": "application/json"}
    )
    yield context
    context.dispose()

# ------------------------------
# UI FIXTURES
# ------------------------------


@pytest.fixture(scope="function")
def ui_context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    Provides a fresh browser context per test.
    """
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture(scope="function")
def ui_page_with_context(ui_context: BrowserContext) -> Generator[Page, None, None]:
    """
    Provides a Playwright page inside a fresh context.
    """
    page = ui_context.new_page()
    yield page
    page.close()


# ------------------------------
# USER FIXTURE (E2E ready)
# ------------------------------

MAX_RETRIES = 3  # כמה פעמים לנסות ליצור יוזר


@pytest.fixture
def new_user(api_request) -> Generator[dict, None, None]:
    """
    Creates a new user with retry logic and cleans up automatically.
    """
    client = AccountClient(api_request)

    for attempt in range(1, MAX_RETRIES + 1):
        username = f"user_{uuid.uuid4().hex[:8]}"
        password = "Password123!"
        print(f"🔥 Attempt {attempt}: Creating username {username}")

        resp = client.create_user(username, password)
        if resp is None:
            print("⚠️ API returned None, retrying...")
            continue

        status = getattr(resp, "status", None)
        if status == 201:
            print("✅ User created successfully!")
            user_id = resp.json().get("userID")
            break
        else:
            print(
                f"⚠️ Failed to create user: status={status}, response={resp.text()}")
            time.sleep(1)
    else:
        raise Exception("Failed to create user after multiple attempts")

    yield {"username": username, "password": password, "user_id": user_id}

    # Cleanup safely
    try:
        token_resp = client.generate_token(username, password)
        token = token_resp.json().get("token")
        if token:
            client.delete_user(user_id, token)
            print(f"🗑️ User {username} deleted in cleanup")
    except Exception as e:
        print("⚠️ Cleanup failed:", e)

# ------------------------------
# BOOKSTORE CLIENT FIXTURE
# ------------------------------


@pytest.fixture
def bookstore_client(api_request, new_user):
    """
    Returns a BookStoreClient instance for the new user.
    """
    from api.clients.bookstore_client import BookStoreClient
    client = BookStoreClient(api_request)
    yield client, new_user
