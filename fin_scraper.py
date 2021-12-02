from bs4 import BeautifulSoup
import requests
from io import StringIO
import csv
import pandas as pd
import time
import datetime
import requests

class FinScraper:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',  # Do Not Track Request Header
        'Connection': 'close'
    }
    __tickers = ''

    def __init__(self, ticker):
        self.ticker = ticker

    def __int__(self, tickers={}):
        self.__tickers = tickers

    def set_tickers(self,tickers):
        self.__tickers = tickers

    def get_tickers(self):
        return self.__tickers

    def resp_to_list(self,resp):
        '''
        :param resp: It takes the body from hist_data.
        :return: This function returns a nested list of the first 5 rows in the table of historical data.
        It can function as a pd head().
        '''
        lst = []
        file = StringIO(resp)
        reader = csv.reader(file)
        data = list(reader)
        for row in data[:5]:
            lst.append(row)
        print(lst)

    def hist_data(self):
        '''
        First model of historical data scraping from yfinance. It uses range instead of specifying dates.
        :return: It returns a requests.Response object with all of the inquired historical data
        '''

        hist_url = f"https://query1.finance.yahoo.com/v7/finance/download/{self.ticker}?"
        hist_params = {
            'range': '5y',
            'interval': '1wk',
            'events': 'history',
            'includeAdjustedClose': 'true'
        }
        resp = requests.get(hist_url, params=hist_params, headers=self.headers, timeout=4).text
        self.resp_to_list(resp)
        return resp

    def hist_data2(self):
        '''
        Second model of historical data scraping from yfinance. It uses dates.
        :return: It returns a pd.Dataframe object with all of the inquired historical data.
        '''
        period1 = int(time.mktime(datetime.datetime(2020, 12, 1, 23, 59).timetuple()))
        period2 = int(time.mktime(datetime.datetime(2020, 12, 31, 23, 59).timetuple()))
        interval = '1wk'

        hist_url = f"https://query1.finance.yahoo.com/v7/finance/download/{self.ticker}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true"
        df = pd.read_csv(hist_url)
        return df

    def scraper(self):
        '''
        :return: Dataframe with market data for a specific stock
        '''
        # df = pd.read_html(url)

        print('Starting scraping...')
        #url = f"http://finance.yahoo.com/quote/{self.ticker}/key-statistics?p={self.ticker}"
        url = f"https://finance.yahoo.com/quote/{self.ticker}?p={self.ticker}"

        resp = requests.get(url, headers=self.headers, timeout=4).text
        sp = BeautifulSoup(resp, 'html.parser')
        # TODO: (1) Complete scraper for one stock
        #  --> TODO: From resp body parse tags with information related to : Close, Open, Low, High, Volume
        # TODO: (2) Complete scraper for more stocks using tickers
        print('Scraping finished!')
        return resp