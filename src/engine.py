from utils.webdriver_setup import WebDriverFactory
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from utils.logger import Logger
from tenacity import retry, stop_after_attempt, wait_fixed

URL = 'https://finance.yahoo.com/research-hub/screener/equity/'

class ScraperEngine:

    def __init__(self):
        self.driver = None
        self.wait = None
        self.logger = None

    def __enter__(self) -> ScraperEngine:
        self.driver = WebDriverFactory.create_headless_chrome_driver()
        self.wait = WebDriverWait(self.driver, 10)   
        self.logger = Logger.get_logger()
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.driver:
            self.logger.info("Fechando driver.")
            self.driver.quit()

    @retry()
    def start_navigation(self):
        try:
            self.driver.get(URL)
        except Exception as e:
            self.logger.error(f"Erro ao carregar a página: {e}")
            raise

    def apply_filter(self, region):

        try:

            self._open_region_menu()
            self._uncheck_all()

            self.logger.debug("Procurando filtro de país")
            locator = (By.XPATH, f"//label[contains(., '{region}')]")
            label = self.wait.until(EC.element_to_be_clickable(locator))
            label.click()

            self.logger.debug("Procurando botão de apply")
            locator = (By.XPATH, f"//button[contains(., 'Apply')]")
            button = self.wait.until(EC.element_to_be_clickable(locator))
            button.click()

            self.wait.until(EC.invisibility_of_element_located((By.XPATH, "//*[contains(text(), 'Apply')]")))

        except Exception as e:
            self.logger.error(f"Ocorreu um erro na rotina de aplicação de filtro. Exceção: {e}")
            raise

    def get_next_page(self):
        try:
            wait = WebDriverWait(self.driver, 10)
            while True:
                yield self.driver.page_source
                botao_next = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Goto next page']")
                if not botao_next or not botao_next.is_enabled():
                    break
                symbol_before = self.driver.find_element(By.CSS_SELECTOR, "table tbody tr td").text
                self.driver.execute_script("arguments[0].click();", botao_next)
                wait.until_not(
                    EC.text_to_be_present_in_element((By.CSS_SELECTOR, "table tbody tr td"),symbol_before)
                )
            return None
        except Exception as e:
            self.logger.error(f"Aconteceu um erro enquanto buscava as páginas: {e}")
            raise


    def _uncheck_all(self):

        try:
            
            checkboxes = self.driver.find_elements(By.XPATH, "//input[@type='checkbox']")
            for checkbox in checkboxes: 
                if checkbox.is_selected() and checkbox.is_displayed():
                    self.driver.execute_script("arguments[0].click();", checkbox)

        except Exception as e:
            self.logger.error(f"Erro ao tentar desmarcar os checkboxes: {e}")
            raise

    def _open_region_menu(self):
        locator = (By.XPATH, "//button[contains(., 'Region')]")
        button = self.wait.until(EC.element_to_be_clickable(locator))
        
        for _ in range(3):
            button.click()
            try:
                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search...']")))
                return True
            except Exception as e:
                self.logger.error(f"Houve um erro ao abrir o menu região: {e}")
                raise
        return False

    