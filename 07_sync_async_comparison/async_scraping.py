import sys
import json
import time
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class YahooScraper(object):
    def __init__(self, urls):
        self.urls = urls
        # Global Place To Store The Data:
        self.all_data = []
        self.master_dict = {}
        # Run The Scraper:
        asyncio.run(self.main())

    async def fetch(self, session, url):
        try:
            async with session.get(url) as response:
                # 1. Extracting the Text:
                text = await response.read()
                # 2. Extracting the Description:
                info = await self.extract_description(text)
                return info

        except Exception as e:
            print(str(e))

    @staticmethod
    async def extract_description(text):
        try:
            soup = BeautifulSoup(text.decode('utf-8'), 'html.parser')
            pattern = re.compile(r'\s--\sData\s--\s')
            script_data = soup.find('script', text=pattern).contents[0]
            start = script_data.find("context") - 2
            json_data = json.loads(script_data[start:-12])

            name = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['price']['longName']
            sector = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile']['sector']
            description = json_data['context']['dispatcher']['stores']['QuoteSummaryStore']['assetProfile'][
                'longBusinessSummary']
            print('ticker added')
            data = {'name': name, 'sector': sector, 'description': description}
            return data

        except Exception as e:
            print('ticker excluded', str(e))

        # time.sleep(0.4)

    async def main(self):
        tasks = []
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"}
        async with aiohttp.ClientSession(headers=headers) as session:
            for url in self.urls:
                tasks.append(self.fetch(session, url))

            htmls = await asyncio.gather(*tasks)

            final_data = []
            for html in htmls:
                if html is not None:
                    final_data.append(html)

            count = len(final_data)
            print("Results:", len(htmls), "tickers", count, "added and", len(htmls) - count, "not found")

            # save the data list into a JSON file
            with open('async_data.json', 'w') as f:
                json.dump(final_data, f)


def main():
    start = time.time()

    # get scraped data
    tickers = []
    exchange = 'amex'
    with open(f'data_ticker/{exchange}.json', encoding='utf-8') as file:
        tickers += json.load(file)

    # filter scraped data for tickers
    symbols_countries = []
    for ticker in tickers:
        symbols_countries.append(ticker[1])

    # insert tickers in destination url
    urls_list = []
    for symbol_country in symbols_countries:
        urls_list.append(f"https://finance.yahoo.com/quote/{symbol_country}/profile?p={symbol_country}")

    # scrape destination url
    YahooScraper(urls=urls_list)

    end = time.time()
    print("Took {} seconds.".format(end - start))


if __name__ == "__main__":
    main()