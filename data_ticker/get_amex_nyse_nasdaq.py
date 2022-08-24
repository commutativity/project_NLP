import requests
import pandas as pd
import string
from bs4 import BeautifulSoup


exchanges = [{'exchange': 'nasdaq', 'url': 'https://www.advfn.com/nasdaq/nasdaq.asp?companies='},
             {'exchange': 'nyse', 'url': 'https://www.advfn.com/nyse/newyorkstockexchange.asp?companies='},
             {'exchange': 'amex', 'url': 'https://www.advfn.com/amex/americanstockexchange.asp?companies='}]


for exchange in exchanges:
    data = pd.DataFrame(columns=['name', 'ticker'])

    company_name, company_ticker = [], []

    for char in string.ascii_uppercase:
        letter = char.upper()
        url = exchange['url']+letter

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                 '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        page = requests.get(url, headers=headers)

        soup = BeautifulSoup(page.text, 'html.parser')
        odd_rows = soup.find_all('tr', attrs={'class': 'ts0'})
        even_rows = soup.find_all('tr', attrs={'class': 'ts1'})

        for i in odd_rows:
            row = i.find_all('td')
            company_name.append(row[0].text.strip())    # company name
            company_ticker.append(row[1].text.strip())  # ticker

        for i in even_rows:
            row = i.find_all('td')
            company_name.append(row[0].text.strip())    # company name
            company_ticker.append(row[1].text.strip())  # ticker

    data['name'] = company_name
    data['ticker'] = company_ticker

    info = exchange['exchange']
    data.to_json(f'data_ticker/{info}.json', orient='values')
