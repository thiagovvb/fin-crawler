from engine import ScraperEngine
from parser import PageParser
import pandas as pd
import csv

scraper = ScraperEngine()
parser = PageParser()
scraper.start_navigation()
scraper.apply_filter("Brazil")
data = []
for page in scraper.get_next_page():
    data.extend(parser.extract_table_data(page))

df = pd.DataFrame(data)
df.to_csv("out.csv", index=False,quoting=csv.QUOTE_ALL)