from bs4 import BeautifulSoup
import requests
from io import StringIO
import csv
import pandas as pd
import time
import datetime
import requests
import re

class FinScraper:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',  # Do Not Track Request Header
        'Connection': 'close'
    }

    def __init__(self, ticker):
        self.ticker = ticker

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

    def hist_data_obj(self):
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

    def hist_data(self,symbol):
        '''
        Second model of historical data scraping from yfinance. It uses dates.
        :return: It returns a pd.Dataframe object with all of the inquired historical data.
        '''
        print(symbol)
        period1 = int(time.mktime(datetime.datetime(2020, 12, 1, 23, 59).timetuple()))
        period2 = int(time.mktime(datetime.datetime(2020, 12, 31, 23, 59).timetuple()))
        interval = '1wk'

        hist_url = f"https://query1.finance.yahoo.com/v7/finance/download/{symbol}?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true"
        df = pd.read_csv(hist_url)
        return df

    def scraper(self):
        '''
        :return: List with market data for a specific stock
        format: Symbol, Price, Close, MarketCap, Volume, P/ERatio, Divident, PrimaryExchange, CDP, CEO, Founded, HQ, Website, Employees, [DayRange (min-max), YearRange(min-max)]
        '''
        # df = pd.read_html(url)
        #url = f"https://www.google.com/finance/quote/{self.ticker}:NASDAQ"
        url = f"https://www.google.com/finance?q={self.ticker}"
        url_open = f"https://www.google.com/search?client=firefox-b-d&q={self.ticker}+stock+open"
        #url = f"http://finance.yahoo.com/quote/{self.ticker}/key-statistics?p={self.ticker}"
        #url = f"https://finance.yahoo.com/quote/{self.ticker}?p={self.ticker}"

        resp = requests.get(url, headers=self.headers, timeout=4).text
        sp = BeautifulSoup(resp, 'html.parser')

        # Cleaning Up Scraped Results

        price = float(sp.find('div',{'class':'YMlKec fxKbKc'}).text.replace('$',''))
        data = sp.find_all('div',{'class':'P6K39c'})[:5]
        try:
            market_status = sp.find_all('div',{'class':'ygUjEc'})[1].text.partition(':')[0]
        except:
            market_status = 'Open'
        print(market_status)
        name = sp.find('div',{'class':'zzDege'}).text.split(' ')[0]
        symbol = sp.find('div',{'class':'PdOqHc'}).text.split('•')[0].replace(' ','')
        print(symbol)

        pattern = re.compile(r'[^\d.]+')
        data = [item.text.replace('$','') for item in data]
        print(data)
        if(market_status!='Closed'):
            close = float(data[0])
            day_range = data[1].split(' - ')
            day_range = [float(item) for item in day_range]
            year_range = data[2].split(' - ')
            year_range = [float(item) for item in year_range]
            market_cap = float(pattern.sub('',data[3]))
            #volume = float(pattern.sub('',data[4]))
            volume = data[4]

            resp = requests.get(url_open,headers=self.headers, timeout=4).text
            sp = BeautifulSoup(resp, 'html.parser')

            open = sp.find('td', {'class': 'iyjjgb'}).text.replace(',', '.')
            if open!='-':
                open = float(open)
            lst = [symbol, market_status, price, open, close, market_cap, volume, name]
            lst.extend(day_range)
            lst.extend(year_range)
        else:
            close = float(data[0])
            year_range = data[1].split(' - ')
            year_range = [float(item) for item in year_range]
            market_cap = float(pattern.sub('', data[2]))
            # volume = float(pattern.sub('',data[4]))
            volume = data[3]

            resp = requests.get(url_open, headers=self.headers, timeout=4).text
            sp = BeautifulSoup(resp, 'html.parser')

            open = sp.find('td', {'class': 'iyjjgb'}).text.replace(',', '.')
            if open!='-':
                open = float(open)
            lst = [symbol, market_status, price, open, close, market_cap, volume, name]
            lst.extend(year_range)

        return lst
