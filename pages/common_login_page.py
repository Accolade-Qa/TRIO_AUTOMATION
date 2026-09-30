import logging
import re
import time
from datetime import datetime

from pages.common_base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.logger = logging.getLogger(self.__class__.__name__)

        # ✅ Enable locators
        self.username = page.locator("input[placeholder*='Your Email Address']")
        self.password = page.locator("input[placeholder*='Password']")
        self.login_btn = page.get_by_role(
            "button", name=re.compile(r"Sign in", re.IGNORECASE)
        )
        self.errormsg = page.get_by_text("Minimum 6 characters required.")
        self.email_error = page.get_by_text(
            "Please enter a valid Email ID.", exact=True
        )
        self.password_error = page.get_by_text(
            "Minimum 6 characters required.", exact=True
        )
        self.wrongusername = page.get_by_text(
            "Minimum 6 characters required.", exact=True
        )
        self.emptyusername = page.locator("mat-error")
        self.page_title1 = page.locator("div.site-name-text-section:visible")
        self.footer = page.locator("div.footer-col.footer-left")
        self.footer_links = page.locator("b:has-text('Accolade Electronics Pvt. Ltd.')")
        self.build_version = page.locator("body app-root app-footer span:nth-child(1)")
        self.valid_email_error = page.locator("mat-error")

    # 🔹 Open Login Page
    # def load(self, url=BASE_URL):
    #     self.page.goto(url, timeout=60000)
    #     self.page.wait_for_load_state("domcontentloaded")

    def load(self, url):
        self.logger.info(f"Opening URL: {url}")
        self.page.goto(url, wait_until="domcontentloaded", timeout=60000)

    def login(self, username, password, wait_for_networkidle=True):
        self.logger.info("Entering username")
        self.username.fill(username)
        self.logger.info("Entering password")
        self.password.fill(password)
        self.logger.info("Clicking login button")
        self.login_btn.click()
        if wait_for_networkidle:
            self.page.wait_for_load_state("networkidle")
        self.logger.info("Login action completed")

    def set_network_offline(self, offline: bool):
        self.logger.info("Setting network offline=%s", offline)
        self.page.context.set_offline(offline)

    # 🔹 New Method 2: Invalid Login Method
    def login_with_invalid_credentials(self, username, password):
        self.logger.info(f"Login started | Username: {username}")
        self.username.fill(username)
        self.password.fill(password)
        self.login_btn.click()
        self.errormsg.wait_for(state="visible", timeout=5000)
        return self.errormsg.inner_text().strip()

    #  🔹 New Method 3: Login with username
    def login_with_usernameonly(self, username):
        self.username.fill(username)
        self.page.keyboard.press("Tab")
        self.login_btn.click()
        self.wrongusername.wait_for(state="visible", timeout=5000)
        error_text = self.wrongusername.inner_text().strip()
        print(f"Captured Error: [{error_text}]")
        return error_text

    def login_with_passwordonly(self, username, password):
        try:
            self.logger.info(f"Login with password only: {password}")
            # Fill fields
            self.username.fill(username)
            self.password.fill(password)
            self.login_btn.click()
            # Wait for error message
            self.emptyusername.first.wait_for(state="visible", timeout=5000)
            error_text = self.emptyusername.first.inner_text().strip()
            print(f"Captured Error: [{error_text}]")  # 🔥 print output
            self.logger.info(f"Captured Error: {error_text}")
            return error_text
        except Exception as e:
            self.logger.error(f"Error in password-only login: {e}")
            raise

    def verify_page_title(self, page_title):
        try:
            self.logger.info("Verifying page title...")
            self.page.wait_for_load_state("load")
            actual_title = self.get_page_title()
            self.logger.info(f"Actual Title: {actual_title}")
            self.logger.info(f"Expected Title: {page_title}")
            return actual_title
        except Exception as e:
            self.logger.error(f"Error while verifying page title: {e}")
            raise

    def get_error_message(self):
        self.logger.info("Fetching error messages...")
        messages = []
        try:
            # ✅ Wait for mat-error to appear
            self.page.wait_for_selector("mat-error", timeout=5000)
            errors = self.page.locator("mat-error")
            count = errors.count()
            self.logger.info(f"Total error messages found: {count}")
            for i in range(count):
                text = errors.nth(i).inner_text().strip()
                if text:
                    messages.append(text)
                    self.logger.info(f"Error {i+1}: {text}")
            return messages
        except Exception as e:
            self.logger.error(f"No error messages found: {str(e)}")
            return []

        # 🔹 Wait for footer

    def verify_footer_links_present(self):
        try:
            self.logger.info("Verifying footer links...")
            # ✅ Use locator directly
            links = self.footer_links
            count = links.count()
            self.logger.info(f"Total footer elements found: {count}")
            assert count > 0, "Footer text not found"
            link_texts = []
            for i in range(count):
                text = links.nth(i).inner_text().strip()
                link_texts.append(text)
                self.logger.info(f"Element {i+1}: {text}")
            return link_texts
        except Exception as e:
            self.logger.error(f"Footer verification failed: {str(e)}")
            raise

    def verify_footer_links_clickable(self):
        try:
            self.logger.info("Verifying footer links are clickable...")
            self.footer.wait_for(state="visible", timeout=5000)
            links = self.footer_links
            count = links.count()
            self.logger.info(f"Total footer links: {count}")
            assert count > 0, "No footer links found"
            results = []
            for i in range(count):
                element = links.nth(i)
                text = element.inner_text().strip()
                is_clickable = element.is_enabled()
                self.logger.info(f"Link {i+1}: {text} | Clickable: {is_clickable}")
                results.append({"text": text, "clickable": is_clickable})
            return results
        except Exception as e:
            self.logger.error(f"Footer clickable verification failed: {str(e)}")
            raise

    def verify_footer_year(self):
        try:
            self.logger.info("Verifying footer year...")
            self.footer.wait_for(state="visible", timeout=5000)
            text = self.footer.inner_text().strip()
            current_year = str(datetime.now().year)
            self.logger.info(f"Footer Text: {text}")
            self.logger.info(f"Expected Year: {current_year}")
            return text, current_year
        except Exception as e:
            self.logger.error(f"Footer year verification failed: {str(e)}")
            raise

    def get_build_version(self):

        try:
            self.logger.info("Fetching build version...")
            self.build_version.wait_for(state="visible", timeout=5000)
            text = self.build_version.inner_text().strip()
            self.logger.info(f"Build Version Found: {text}")
            return text
        except Exception as e:
            self.logger.error(f"Failed to get build version: {str(e)}")
            raise
