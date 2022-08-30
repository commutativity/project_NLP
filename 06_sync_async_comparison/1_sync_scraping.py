import json
import time
import re
import requests
from bs4 import BeautifulSoup


def yahoo_scraper():
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"}

    tickers = []
    exchange = 'amex'
    with open(f'../02_data_ticker/{exchange}.json', encoding='utf-8') as file:
        tickers += json.load(file)

    url = 'https://finance.yahoo.com/quote/{}/profile?p={}'
    data = []
    count = 1

    for row in tickers:
        try:
            symbol = row[1]
            response = requests.get(url.format(symbol, symbol), headers=headers)  # url profile website is scraped

            soup = BeautifulSoup(response.text, 'html.parser')
            pattern = re.compile(r'\s--\sData\s--\s')
            script_data = soup.find('script', text=pattern).contents[0]
            start = script_data.find("context")-2
            json_data = json.loads(script_data[start:-12])

            sector = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile']['sector']
            description = (json_data['context']['dispatcher']['stores']['QuoteSummaryStore']
                                    ['assetProfile']['longBusinessSummary'])

            data.append({"name": row[0], 'sector': sector, "description": description})
            print("added: ", row[0])
            count += 1

        except KeyError as e:
            print("not found: ", row[0], str(e))

    print("Results:", len(tickers), "tickers", count, "added and", len(tickers)-count, "not found")

    # save the data list into a JSON file
    with open('sync_data.json', 'w') as f:
        json.dump(data, f)


def main():
    start = time.time()
    yahoo_scraper()
    end = time.time()
    print("Took {} seconds.".format(end - start))


if __name__ == "__main__":
    main()