from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Scraping:
    def __init__(self,scrap_code:str,browser_url):
        self.scrap_code = scrap_code
        self.browser_url = browser_url
        self.options = Options()
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--headless")
        self.options.add_argument('--disable-dev-shm-usage')
    
    