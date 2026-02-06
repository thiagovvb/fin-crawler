from utils.webdriver_setup import WebDriverFactory
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

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
            raise

    def apply_filter(self, region):

        try:

            self._open_region_menu()
            self._uncheck_all()

            print("Searching for country filter...")
            locator = (By.XPATH, f"//label[contains(., '{region}')]")
            label = self.wait.until(EC.element_to_be_clickable(locator))
            label.click()

            print("Searching for apply button...")
            locator = (By.XPATH, f"//button[contains(., 'Apply')]")
            button = self.wait.until(EC.element_to_be_clickable(locator))
            button.click()

            self.wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Apply')]")))

            time.sleep(10)

        except Exception as e:
            print(f"Problema ao aplicar filtro: {e}")
            raise


    def _uncheck_all(self):

        try:
            
            checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
            for checkbox in checkboxes: 
                if checkbox.is_selected() and checkbox.is_displayed():
                    print("Achou uma selecionada")
                    parent_text = checkbox.find_element(By.XPATH, "..").text
                    print(f"Checkbox selecionada: {parent_text}")
                    self.driver.execute_script("arguments[0].click();", checkbox)

        except Exception as e:
            print(f"Erro ao tentar desmarcar os checkboxes: {e}")
            raise

    def _open_region_menu(self):
        locator = (By.XPATH, "//button[contains(., 'Region')]")
        button = self.wait.until(EC.element_to_be_clickable(locator))
        
        for _ in range(3):
            button.click()
            try:
                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search...']")))
                return True
            except:
                print("Clique não abriu o menu, tentando novamente...")
        return False

    