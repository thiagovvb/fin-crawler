from engine import ScraperEngine
from parser import PageParser
import pandas as pd
import csv
import sys

def main():

    filter = sys.argv[1]

    scraper = ScraperEngine()
    parser = PageParser()

    scraper.start_navigation()
    scraper.apply_filter(filter)

    data = []
    for page in scraper.get_next_page():
        data.extend(parser.extract_table_data(page))

    df = pd.DataFrame(data)
    df.to_csv("output.csv", index=False,quoting=csv.QUOTE_ALL)

main()