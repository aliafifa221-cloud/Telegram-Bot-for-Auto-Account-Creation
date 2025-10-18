"""
Alternative automation module using Playwright for account creation
Provides better Cloudflare bypass than Selenium in some cases
"""

import logging
import time
import random
import string
from typing import Dict, Optional
from datetime import datetime

from playwright.sync_api import sync_playwright, Browser, Page, TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)


class AccountCreatorPlaywright:
    """Handles automated account creation using Playwright"""

    def __init__(
        self,
        dashboard_url: str,
        dashboard_username: str,
        dashboard_password: str,
        parent_value: str,
        headless: bool = True,
        timeout: int = 30
    ):
        """
        Initialize the account creator with Playwright
        
        Args:
            dashboard_url: URL of the dashboard
            dashboard_username: Username for dashboard login
            dashboard_password: Password for dashboard login
            parent_value: Fixed parent value for account creation
            headless: Whether to run browser in headless mode
            timeout: Default timeout for operations
        """
        self.dashboard_url = dashboard_url
        self.dashboard_username = dashboard_username
        self.dashboard_password = dashboard_password
        self.parent_value = parent_value
        self.headless = headless
        self.timeout = timeout * 1000  # Playwright uses milliseconds

    def _generate_email(self, username: str) -> str:
        """Generate a unique email address"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        return f"{username}_{timestamp}_{random_suffix}@temp.mail"

    def _wait_for_cloudflare(self, page: Page, max_wait: int = 30) -> bool:
        """
        Wait for Cloudflare protection to pass
        
        Args:
            page: Playwright page object
            max_wait: Maximum time to wait in seconds
            
        Returns:
            True if Cloudflare check passed, False otherwise
        """
        logger.info('Checking for Cloudflare protection...')
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            try:
                page_title = page.title().lower()
                
                # Check if we're still on Cloudflare page
                if 'cloudflare' in page_title or 'just a moment' in page_title:
                    logger.info('Cloudflare protection detected, waiting...')
                    time.sleep(2)
                    continue
                
                # Check if we've reached the actual page
                if 'dashboard' in page_title or 'login' in page_title:
                    logger.info('Cloudflare check passed!')
                    return True
                    
            except Exception as e:
                logger.warning(f'Error checking Cloudflare: {e}')
            
            time.sleep(1)
        
        logger.warning('Cloudflare wait timeout')
        return False

    def _login(self, page: Page) -> bool:
        """
        Login to the dashboard
        
        Args:
            page: Playwright page object
            
        Returns:
            True if login successful, False otherwise
        """
        try:
            logger.info(f'Navigating to {self.dashboard_url}')
            page.goto(self.dashboard_url, timeout=self.timeout)
            
            # Wait for Cloudflare if present
            self._wait_for_cloudflare(page)
            
            # Wait for page to settle
            page.wait_for_load_state('networkidle')
            time.sleep(2)
            
            # Try to find and fill login form
            # Common username/email field selectors
            username_selectors = [
                '#username',
                '#email',
                'input[name="username"]',
                'input[name="email"]',
                'input[type="text"]',
                'input[type="email"]',
            ]
            
            username_field = None
            for selector in username_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        username_field = page.locator(selector).first
                        logger.info(f'Found username field with selector: {selector}')
                        break
                except Exception:
                    continue
            
            if not username_field:
                logger.error('Could not find username field')
                return False
            
            # Common password field selectors
            password_selectors = [
                '#password',
                'input[name="password"]',
                'input[type="password"]',
            ]
            
            password_field = None
            for selector in password_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        password_field = page.locator(selector).first
                        logger.info(f'Found password field with selector: {selector}')
                        break
                except Exception:
                    continue
            
            if not password_field:
                logger.error('Could not find password field')
                return False
            
            # Enter credentials
            logger.info('Entering credentials...')
            username_field.fill(self.dashboard_username)
            time.sleep(0.5)
            password_field.fill(self.dashboard_password)
            time.sleep(0.5)
            
            # Find and click login button
            login_button_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Login")',
                'button:has-text("Sign in")',
            ]
            
            for selector in login_button_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.click()
                        logger.info(f'Clicked login button with selector: {selector}')
                        break
                except Exception:
                    continue
            
            # Wait for navigation after login
            page.wait_for_load_state('networkidle')
            time.sleep(3)
            
            # Check if login was successful
            current_url = page.url
            if 'login' not in current_url.lower() or 'dashboard' in current_url.lower():
                logger.info('Login successful!')
                return True
            else:
                logger.error('Login may have failed')
                return False
                
        except Exception as e:
            logger.error(f'Error during login: {e}', exc_info=True)
            return False

    def _navigate_to_player_creation(self, page: Page) -> bool:
        """
        Navigate to player creation page
        
        Args:
            page: Playwright page object
            
        Returns:
            True if navigation successful, False otherwise
        """
        try:
            # Try finding a link to player creation
            link_texts = [
                'Create Player',
                'Add Player',
                'New Player',
                'Create Account',
            ]
            
            for text in link_texts:
                try:
                    if page.locator(f'text={text}').count() > 0:
                        page.locator(f'text={text}').first.click()
                        logger.info(f'Clicked link: {text}')
                        page.wait_for_load_state('networkidle')
                        time.sleep(2)
                        return True
                except Exception:
                    continue
            
            # Try direct navigation to common URLs
            player_create_urls = [
                f'{self.dashboard_url}/players/create',
                f'{self.dashboard_url}/player/create',
                f'{self.dashboard_url}/create-player',
                f'{self.dashboard_url}/add-player',
            ]
            
            for url in player_create_urls:
                try:
                    logger.info(f'Trying to navigate to: {url}')
                    page.goto(url, timeout=self.timeout)
                    page.wait_for_load_state('networkidle')
                    time.sleep(2)
                    
                    current_url = page.url.lower()
                    if 'create' in current_url or 'add' in current_url:
                        logger.info('Successfully navigated to player creation page')
                        return True
                except Exception as e:
                    logger.warning(f'Failed to navigate to {url}: {e}')
                    continue
            
            logger.error('Could not navigate to player creation page')
            return False
            
        except Exception as e:
            logger.error(f'Error navigating to player creation: {e}', exc_info=True)
            return False

    def _fill_and_submit_form(
        self,
        page: Page,
        mobile: str,
        username: str,
        password: str,
        email: str
    ) -> bool:
        """
        Fill and submit the player creation form
        
        Args:
            page: Playwright page object
            mobile: Mobile number
            username: Username
            password: Password
            email: Email address
            
        Returns:
            True if form submitted successfully, False otherwise
        """
        try:
            # Field mappings
            fields_to_fill = {
                'mobile': mobile,
                'phone': mobile,
                'mobile_number': mobile,
                'username': username,
                'user_name': username,
                'email': email,
                'email_address': email,
                'password': password,
                'parent': self.parent_value,
                'parent_id': self.parent_value,
                'parent_user': self.parent_value,
            }
            
            # Try to fill each field
            for field_name, value in fields_to_fill.items():
                selectors = [
                    f'input[name="{field_name}"]',
                    f'input[id="{field_name}"]',
                    f'#{field_name}',
                    f'[name="{field_name}"]',
                ]
                
                for selector in selectors:
                    try:
                        if page.locator(selector).count() > 0:
                            page.locator(selector).first.fill(value)
                            logger.info(f'Filled field: {field_name} = {value}')
                            time.sleep(0.3)
                            break
                    except Exception:
                        continue
            
            # Take screenshot before submitting
            try:
                page.screenshot(path='/tmp/playwright_before_submit.png')
                logger.info('Screenshot saved: /tmp/playwright_before_submit.png')
            except Exception:
                pass
            
            # Find and click submit button
            submit_selectors = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Submit")',
                'button:has-text("Create")',
                'button:has-text("Save")',
            ]
            
            for selector in submit_selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).first.click()
                        logger.info(f'Submit button clicked with selector: {selector}')
                        page.wait_for_load_state('networkidle')
                        time.sleep(3)
                        return True
                except Exception:
                    continue
            
            logger.error('Could not find submit button')
            return False
            
        except Exception as e:
            logger.error(f'Error filling form: {e}', exc_info=True)
            return False

    def create_account(
        self,
        mobile: str,
        username: str,
        password: str
    ) -> Dict[str, any]:
        """
        Main method to create an account using Playwright
        
        Args:
            mobile: Mobile number
            username: Username
            password: Password
            
        Returns:
            Dictionary with success status and details
        """
        result = {
            'success': False,
            'error': None,
            'email': None,
            'parent': self.parent_value
        }
        
        playwright = None
        browser = None
        
        try:
            # Generate email
            email = self._generate_email(username)
            result['email'] = email
            
            logger.info(f'Starting account creation for username: {username}')
            
            # Set up Playwright
            playwright = sync_playwright().start()
            browser = playwright.chromium.launch(
                headless=self.headless,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                ]
            )
            
            # Create context with realistic settings
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )
            
            # Add init script to hide automation
            context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
            
            page = context.new_page()
            page.set_default_timeout(self.timeout)
            
            # Login to dashboard
            if not self._login(page):
                result['error'] = 'Failed to login to dashboard'
                return result
            
            # Navigate to player creation page
            if not self._navigate_to_player_creation(page):
                result['error'] = 'Failed to navigate to player creation page'
                return result
            
            # Fill and submit form
            if not self._fill_and_submit_form(page, mobile, username, password, email):
                result['error'] = 'Failed to fill and submit form'
                return result
            
            # Check for success message or error
            page_content = page.content().lower()
            
            if 'success' in page_content or 'created' in page_content:
                result['success'] = True
                logger.info('Account created successfully!')
            elif 'error' in page_content or 'failed' in page_content:
                result['error'] = 'Form submission returned an error'
            else:
                # Assume success if no error detected
                result['success'] = True
                logger.info('Account creation completed')
            
        except Exception as e:
            error_msg = str(e)
            result['error'] = f'Unexpected error: {error_msg}'
            logger.error(f'Error in create_account: {error_msg}', exc_info=True)
        
        finally:
            # Clean up
            if browser:
                try:
                    browser.close()
                    logger.info('Browser closed')
                except Exception as e:
                    logger.warning(f'Error closing browser: {e}')
            
            if playwright:
                try:
                    playwright.stop()
                except Exception as e:
                    logger.warning(f'Error stopping playwright: {e}')
        
        return result
