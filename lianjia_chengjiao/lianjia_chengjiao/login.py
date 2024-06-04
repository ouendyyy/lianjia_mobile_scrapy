from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException

from lianjia_chengjiao.exceptions import LoginError


class Login:

    login_url = "https://clogin.lianjia.com/login?service=https%3A%2F%2Fwww.lianjia.com%2Fuser%2F" \
                "checklogin%3Fredirect%3Dhttps%253A%252F%252Fsh.lianjia.com%252Fchengjiao%252F"

    def __init__(self):
        self.driver = webdriver.Chrome()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def get_cookies(self) -> dict:
        try:
            self.driver.get(self.login_url)
            wait = WebDriverWait(self.driver, timeout=120)
            wait.until(EC.url_changes(self.driver.current_url))  # wait for manul get_cookies
            cookies = {}
            for item in self.driver.get_cookies():
                cookies[item['name']] = item['value']
            return cookies
        except WebDriverException:
            raise LoginError
