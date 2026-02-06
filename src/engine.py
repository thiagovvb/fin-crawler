from utils.webdriver_setup import WebDriverFactory
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

URL = 'https://finance.yahoo.com/research-hub/screener/equity/'

class ScraperEngine:

    def __init__(self):
        self.driver = WebDriverFactory.create_headless_chrome_driver()
        self.wait = WebDriverWait(self.driver, 10)

    def start_navigation(self):
        try:
            self.driver.get(URL)
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.yf-1uayyp1")))
        except Exception as e:
            print(f"Erro ao carregar a página: {e}")
            self.driver.quit()
            raise

    def apply_filter(self, region):

        try:

            print("Searching for region button...")
            locator = (By.XPATH, "//button[contains(., 'Region')]")
            button = self.wait.until(EC.element_to_be_clickable(locator))
            button.click()

            print("Searching for country filter...")
            locator = (By.XPATH, f"//label[contains(., '{region}')]")
            label = self.wait.until(EC.element_to_be_clickable(locator))
            label.click()

            print("Searching for apply button...")
            locator = (By.XPATH, f"//label[contains(., 'Apply')]")
            button = self.wait.until(EC.element_to_be_clickable(locator))
            button.click()

            self.wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Apply')]")))

        except Exception as e:
            print(f"Problema ao aplicar filtro: {e}")
            raise