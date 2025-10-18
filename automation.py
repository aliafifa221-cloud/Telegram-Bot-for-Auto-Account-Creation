"""
Automation module for account creation
Handles web automation using Selenium with Cloudflare bypass
"""

import logging
import time
import random
import string
from typing import Dict, Optional
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException
)
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


class AccountCreator:
    """Handles automated account creation on ichancy.com dashboard"""

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
        Initialize the account creator
        
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
        self.timeout = timeout
        self.driver: Optional[webdriver.Chrome] = None

    def _setup_driver(self) -> webdriver.Chrome:
        """Set up and configure Chrome WebDriver with Cloudflare bypass options"""
        options = Options()
        
        if self.headless:
            options.add_argument('--headless=new')
        
        # Anti-detection options
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Additional options for stability
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Set up driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Execute CDP commands to bypass detection
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        driver.set_page_load_timeout(self.timeout)
        driver.implicitly_wait(10)
        
        return driver

    def _generate_email(self, username: str) -> str:
        """Generate a unique email address"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        return f"{username}_{timestamp}_{random_suffix}@temp.mail"

    def _wait_for_cloudflare(self, max_wait: int = 30) -> bool:
        """
        Wait for Cloudflare protection to pass
        
        Args:
            max_wait: Maximum time to wait in seconds
            
        Returns:
            True if Cloudflare check passed, False otherwise
        """
        logger.info('Checking for Cloudflare protection...')
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            try:
                # Check if we're still on Cloudflare page
                page_title = self.driver.title.lower()
                page_source = self.driver.page_source.lower()
                
                if 'cloudflare' in page_title or 'just a moment' in page_source:
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

    def _login(self) -> bool:
        """
        Login to the dashboard
        
        Returns:
            True if login successful, False otherwise
        """
        try:
            logger.info(f'Navigating to {self.dashboard_url}')
            self.driver.get(self.dashboard_url)
            
            # Wait for Cloudflare if present
            self._wait_for_cloudflare()
            
            # Wait for login page to load
            time.sleep(3)
            
            # Try to find login form elements
            # Note: These selectors need to be updated based on actual website structure
            wait = WebDriverWait(self.driver, self.timeout)
            
            # Common login field selectors
            username_selectors = [
                (By.ID, 'username'),
                (By.ID, 'email'),
                (By.NAME, 'username'),
                (By.NAME, 'email'),
                (By.CSS_SELECTOR, 'input[type="text"]'),
                (By.CSS_SELECTOR, 'input[type="email"]'),
            ]
            
            password_selectors = [
                (By.ID, 'password'),
                (By.NAME, 'password'),
                (By.CSS_SELECTOR, 'input[type="password"]'),
            ]
            
            username_field = None
            for selector in username_selectors:
                try:
                    username_field = wait.until(EC.presence_of_element_located(selector))
                    logger.info(f'Found username field with selector: {selector}')
                    break
                except TimeoutException:
                    continue
            
            if not username_field:
                logger.error('Could not find username field')
                return False
            
            password_field = None
            for selector in password_selectors:
                try:
                    password_field = self.driver.find_element(*selector)
                    logger.info(f'Found password field with selector: {selector}')
                    break
                except NoSuchElementException:
                    continue
            
            if not password_field:
                logger.error('Could not find password field')
                return False
            
            # Enter credentials
            logger.info('Entering credentials...')
            username_field.clear()
            username_field.send_keys(self.dashboard_username)
            time.sleep(0.5)
            
            password_field.clear()
            password_field.send_keys(self.dashboard_password)
            time.sleep(0.5)
            
            # Find and click login button
            login_button_selectors = [
                (By.CSS_SELECTOR, 'button[type="submit"]'),
                (By.CSS_SELECTOR, 'input[type="submit"]'),
                (By.XPATH, '//button[contains(text(), "Login")]'),
                (By.XPATH, '//button[contains(text(), "Sign in")]'),
                (By.XPATH, '//input[@value="Login"]'),
            ]
            
            login_button = None
            for selector in login_button_selectors:
                try:
                    login_button = self.driver.find_element(*selector)
                    logger.info(f'Found login button with selector: {selector}')
                    break
                except NoSuchElementException:
                    continue
            
            if login_button:
                login_button.click()
                logger.info('Login button clicked')
            else:
                # Try submitting the form
                password_field.submit()
                logger.info('Form submitted')
            
            # Wait for dashboard to load
            time.sleep(5)
            
            # Check if login was successful
            current_url = self.driver.current_url
            if 'login' not in current_url.lower() or 'dashboard' in current_url.lower():
                logger.info('Login successful!')
                return True
            else:
                logger.error('Login may have failed')
                return False
                
        except Exception as e:
            logger.error(f'Error during login: {e}', exc_info=True)
            return False

    def _navigate_to_player_creation(self) -> bool:
        """
        Navigate to player creation page
        
        Returns:
            True if navigation successful, False otherwise
        """
        try:
            # Common URLs for player creation
            player_create_urls = [
                f'{self.dashboard_url}/players/create',
                f'{self.dashboard_url}/player/create',
                f'{self.dashboard_url}/create-player',
                f'{self.dashboard_url}/add-player',
            ]
            
            # Try finding a link to player creation
            link_texts = [
                'Create Player',
                'Add Player',
                'New Player',
                'Create Account',
            ]
            
            for text in link_texts:
                try:
                    link = self.driver.find_element(By.PARTIAL_LINK_TEXT, text)
                    link.click()
                    logger.info(f'Clicked link: {text}')
                    time.sleep(3)
                    return True
                except NoSuchElementException:
                    continue
            
            # Try direct navigation to common URLs
            for url in player_create_urls:
                try:
                    logger.info(f'Trying to navigate to: {url}')
                    self.driver.get(url)
                    time.sleep(3)
                    
                    # Check if we're on a valid page
                    if 'create' in self.driver.current_url.lower() or 'add' in self.driver.current_url.lower():
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
        mobile: str,
        username: str,
        password: str,
        email: str
    ) -> bool:
        """
        Fill and submit the player creation form
        
        Args:
            mobile: Mobile number
            username: Username
            password: Password
            email: Email address
            
        Returns:
            True if form submitted successfully, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, self.timeout)
            
            # Field mappings (name/id: value)
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
                field_selectors = [
                    (By.NAME, field_name),
                    (By.ID, field_name),
                    (By.CSS_SELECTOR, f'input[name="{field_name}"]'),
                    (By.CSS_SELECTOR, f'input[id="{field_name}"]'),
                ]
                
                for selector in field_selectors:
                    try:
                        field = self.driver.find_element(*selector)
                        field.clear()
                        field.send_keys(value)
                        logger.info(f'Filled field: {field_name} = {value}')
                        time.sleep(0.3)
                        break
                    except NoSuchElementException:
                        continue
            
            # Take a screenshot before submitting (for debugging)
            try:
                self.driver.save_screenshot('/tmp/before_submit.png')
                logger.info('Screenshot saved: /tmp/before_submit.png')
            except Exception:
                pass
            
            # Find and click submit button
            submit_selectors = [
                (By.CSS_SELECTOR, 'button[type="submit"]'),
                (By.CSS_SELECTOR, 'input[type="submit"]'),
                (By.XPATH, '//button[contains(text(), "Submit")]'),
                (By.XPATH, '//button[contains(text(), "Create")]'),
                (By.XPATH, '//button[contains(text(), "Save")]'),
            ]
            
            for selector in submit_selectors:
                try:
                    submit_button = self.driver.find_element(*selector)
                    submit_button.click()
                    logger.info(f'Submit button clicked with selector: {selector}')
                    time.sleep(5)
                    return True
                except NoSuchElementException:
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
        Main method to create an account
        
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
        
        try:
            # Generate email
            email = self._generate_email(username)
            result['email'] = email
            
            logger.info(f'Starting account creation for username: {username}')
            
            # Set up driver
            self.driver = self._setup_driver()
            
            # Login to dashboard
            if not self._login():
                result['error'] = 'Failed to login to dashboard'
                return result
            
            # Navigate to player creation page
            if not self._navigate_to_player_creation():
                result['error'] = 'Failed to navigate to player creation page'
                return result
            
            # Fill and submit form
            if not self._fill_and_submit_form(mobile, username, password, email):
                result['error'] = 'Failed to fill and submit form'
                return result
            
            # Check for success message or error
            time.sleep(3)
            page_source = self.driver.page_source.lower()
            
            if 'success' in page_source or 'created' in page_source:
                result['success'] = True
                logger.info('Account created successfully!')
            elif 'error' in page_source or 'failed' in page_source:
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
            if self.driver:
                try:
                    self.driver.quit()
                    logger.info('Browser closed')
                except Exception as e:
                    logger.warning(f'Error closing browser: {e}')
        
        return result
