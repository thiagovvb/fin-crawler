from bs4 import BeautifulSoup

class PageParser:

    def extract_table_data(self, html):
        
        bsoup = BeautifulSoup(html, 'html.parser')
        records = []

        table = bsoup.find('table')
        if not table:
            return []
        
        rows = table.find('tbody').find_all('tr')

        for row in rows:
            cols = row.find_all('td')

            if len(cols) > 1:
                records.append({
                    "symbol": cols[1].text.strip(),
                    "name": cols[2].text.strip(),
                    "price": self._parse_price(cols[4].text.strip())
                })

        return records
    
    def _parse_price(self, text):
        try:
            return float(text.replace(',',''))
        except ValueError:
            return None