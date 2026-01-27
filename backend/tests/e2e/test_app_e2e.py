"""import pytest
from playwright.sync_api import sync_playwright # type: ignore

def test_open_homepage():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:3000")  # React app
        assert "Quiz" in page.title()
        browser.close()"""
