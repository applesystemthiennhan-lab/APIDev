import subprocess
import sys

required_modules = ["selenium", "webdriver_manager"]
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        print(f"[!] Đang cài module: {module}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


class UIManager:

    @staticmethod
    def show_status(message):
        print(f"[✔] {message}")

    @staticmethod
    def show_error(message):
        print(f"[❌] {message}")


class ZefoyBaseException(Exception):

    def __init__(self, message="Zefoy automation error occurred"):
        self.message = message
        super().__init__(self.message)


class AutomationError(ZefoyBaseException):

    def __init__(self, message="Automation process failed"):
        super().__init__(message)


class ElementNotFoundError(ZefoyBaseException):

    def __init__(self, element_description):
        message = f"Element not found: {element_description}"
        super().__init__(message)


class DelayCalculationError(ZefoyBaseException):

    def __init__(self, delay_info):
        message = f"Delay calculation failed: {delay_info}"
        super().__init__(message)


class PageHandler:

    def __init__(self, driver):
        self.driver = driver
        self.locators = {
            'url_input':
            "//div[contains(@class, 't-views-menu')]//input[@type='search' and @placeholder='Enter Video URL']",
            'search_btn':
            "//div[contains(@class, 't-views-menu')]//button[@type='submit' and contains(., 'Search')]",
            'views_section':
            "//div[contains(@class, 'colsmenu')]//h5[normalize-space(text())='Views']/following-sibling::button",
            'views_btn':
            "//div[@id='c2VuZC9mb2xeb3dlcnNfdGlrdG9V']//form//button[@type='submit' and contains(@class, 'wbutton')]"
        }

    def navigate_to_views_section(self):
        self._click_element(self.locators['views_section'])

    def submit_video_url(self, video_url):
        self._input_text(self.locators['url_input'], video_url)
        self._click_element(self.locators['search_btn'])

    def send_views(self):
        try:
            self._click_element(self.locators['search_btn'])
        except:
            pass
        for selector in [
                self.locators['views_btn'],
                "//form//button[contains(@class, 'wbutton') and contains(., 'Submit')]",
                "//form//button[contains(@class, 'wbutton')]"
        ]:
            try:
                self._click_element(selector)
                time.sleep(5)
                break
            except:
                pass
        self._verify_success()

    def _click_element(self, xpath, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath)))
            element.click()
        except Exception as e:
            raise ElementNotFoundError(f"{xpath} - {str(e)}")

    def _input_text(self, xpath, text, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            element.clear()
            element.send_keys(text)
        except Exception as e:
            raise ElementNotFoundError(f"{xpath} - {str(e)}")

    def _verify_success(self, timeout=20):
        success_xpath = "//*[contains(text(), 'Successfully')]"
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, success_xpath)))
        except:
            self.send_views()
            raise ElementNotFoundError("Success message not found")


class TimerHandler:

    def handle_delay(self, driver, max_wait=180):
        try:
            delay_text = self._get_delay_text(driver, max_wait)
            wait_time = self._parse_delay(delay_text) if delay_text else 300
            wait_time = wait_time if wait_time > 0 else 300

            for i in range(wait_time + 5, 0, -1):
                print(f"Waiting {i} seconds...", end="\r")
                time.sleep(1)
        except Exception as e:
            raise DelayCalculationError(str(e))

    def _get_delay_text(self, driver, timeout):
        delay_xpath = "//*[contains(text(), 'Please wait')]"
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, delay_xpath)))
        return element.text

    def _parse_delay(self, text):
        minutes = re.search(r"(\d+)\s*min", text, re.IGNORECASE)
        seconds = re.search(r"(\d+)\s*sec", text, re.IGNORECASE)
        return (int(minutes.group(1)) * 60 if minutes else 0) + (int(
            seconds.group(1)) if seconds else 0)

    def wait_before_retry(self, base=15):
        print(f" Retrying in {base} seconds...")
        time.sleep(base)

    def handle_retry_delay(self):
        print("Error detected, retrying in 5 seconds...")
        time.sleep(5)


class AdHandler:

    def __init__(self, driver):
        self.driver = driver
        self.ui = UIManager()

    def check_for_ads_presence(self, timeout=3):
        return "#google_vignette" in self.driver.current_url

    def handle_ads(self, max_attempts=3):
        self.ui.show_status("🌀 Checking for ads...")
        return True


class ZefoyAutomator:

    def __init__(self, video_url):
        self.driver = self._setup_driver()
        self.page_handler = PageHandler(self.driver)
        self.timer_handler = TimerHandler()
        self.ad_handler = AdHandler(self.driver)
        self.video_url = video_url

        self.driver.get('https://zefoy.com/')
        input(
            " Vui lòng hoàn thành CAPTCHA thủ công và nhấn Enter để tiếp tục..."
        )

    def _setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--start-maximized")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    def run(self):
        while True:
            try:
                self.driver.refresh()
                self.page_handler.navigate_to_views_section()
                self._process_views()
            except Exception as e:
                print(f"Error occurred: {str(e)[:100]}")
                continue

    def _process_views(self):
        try:
            self.page_handler.submit_video_url(self.video_url)
            self.timer_handler.handle_delay(self.driver)

            if self.ad_handler.check_for_ads_presence(timeout=5):
                print("🔍 Ads detected, attempting to handle them...")
                self.ad_handler.handle_ads()
            else:
                print("No ads detected.")

            self.page_handler.send_views()
            print("Successfully sent views!")
            self.timer_handler.wait_before_retry()

        except Exception:
            self.timer_handler.handle_retry_delay()
            raise


def main():
    print("Buff tiktok")
    video_url = input(" Nhập link video TikTok cần buff: ").strip()
    if not video_url.startswith("http"):
        print("Link không hợp lệ. Thoát...")
        return
    print(" Vui lòng hoàn thành CAPTCHA thủ công và nhấn Enter để tiếp tục...")
    try:
        automator = ZefoyAutomator(video_url)
        automator.run()
    except AutomationError as e:
        print(f"Lỗi tự động: {e}")
    except KeyboardInterrupt:
        print("Dừng bởi người dùng.")
    finally:
        automator.driver.quit()
        print("Đã đóng trình duyệt. Kết thúc!")


if __name__ == "__main__":
    main()
