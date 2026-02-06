from engine import ScraperEngine
from parser import PageParser

scraper = ScraperEngine()
parser = PageParser()
scraper.start_navigation()
scraper.apply_filter("Brazil")
print(parser.extract_table_data(scraper.driver.page_source))