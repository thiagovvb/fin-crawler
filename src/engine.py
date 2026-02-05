from utils.webdriver_setup import WebDriverFactory

class ScraperEngine:
    def __init__(self):
        
        self.driver = WebDriverFactory.create_headless_chrome_driver()