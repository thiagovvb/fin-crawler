from engine import ScraperEngine
from parser import PageParser
import pandas as pd
import csv
import sys
from utils.logger import Logger

def main():

    logger = Logger.get_logger()

    if len(sys.argv) <= 1:
        logger.error("Parâmetro não informado")
        return
    
    filter = sys.argv[1]

    with ScraperEngine() as scraper:
        parser = PageParser()

        scraper.start_navigation()
        scraper.apply_filter(filter)

        data = []
        i = 1
        for page in scraper.get_next_page():
            logger.info(f"Processando página {i}")
            data.extend(parser.extract_table_data(page))
            i += 1

        df = pd.DataFrame(data)
        df.to_csv("output.csv", index=False,quoting=csv.QUOTE_ALL)

if __name__ == "__main__":
    main()