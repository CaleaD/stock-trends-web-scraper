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
        :return: List with market data for a specific stock
        format: Symbol, Price, Close, MarketCap, Volume, P/ERatio, Divident, PrimaryExchange, CDP, CEO, Founded, HQ, Website, Employees, [DayRange (min-max), YearRange(min-max)]
        '''
        # df = pd.read_html(url)

        #url = f"https://www.google.com/finance/quote/{self.ticker}:NASDAQ"
        url = f"https://www.google.com/finance?q={self.ticker}"
        #url = f"http://finance.yahoo.com/quote/{self.ticker}/key-statistics?p={self.ticker}"
        #url = f"https://finance.yahoo.com/quote/{self.ticker}?p={self.ticker}"

        resp = requests.get(url, headers=self.headers, timeout=4).text
        sp = BeautifulSoup(resp, 'html.parser')

        title = sp.title.text
        result = sp.findAll('title')

        lst = []
        lst.append(self.ticker)

        # Live update of price
        # for _ in range(100):
        #     html = requests.get(f'https://www.google.com/search?q={self.ticker}+stock', headers=self.headers)
        #     soup = BeautifulSoup(html.text, 'lxml')
        #
        #     print(soup.find('span',{'class':'IsqQVc NprOob wT3VGc'}).text)
        #     time.sleep(20)

        current_price = sp.find('div',{'class':'YMlKec fxKbKc'}).text
        lst.append(current_price)

        # percentage = sp.find('div',{'class':'JwB6zf'}).text #pre-market
        # lst.append(percentage)

        #stop_at = sp.find(class_="IPIeJ")
        #table_values = stop_at.find_all_previous('div',{'class':'P6K39c'})
        table_values = sp.findAll('div',{'class':'P6K39c'})

        for val in table_values:
            lst.append(val.text)


        # Values Clean-Up
        #TODO: May be too many values, fix scraper to scrape fewer values
        # To keep: Symbol, Price, Close, Volume, P/ERatio, Divident, PrimaryExchange, CEO, Founded, Website, [DayRange (min-max), YearRange(min-max)]
        lst.pop()  # We don't want employees anymore
        lst = [s.replace('$',"") for s in lst]
        day_range = lst[3].split(' - ')
        day_range = [float(item) for item in day_range]
        year_range = lst[4].split(' - ')
        year_range = [float(item) for item in year_range]
        lst.remove(lst[3])
        lst.remove(lst[3])
        lst.extend(day_range)
        lst.extend(year_range)
        lst[4] = lst[4].replace("M","")
        lst[6] = lst[6].replace("%","")
        floatable = [1,2,4,5,6] # Price, Close, Vol, PER, Dividents
        for i in floatable:
            lst[i] = float(lst[i])
        lst[10] = datetime.datetime.strptime(lst[10],"%b %d, %Y").strftime("%d-%m-%Y") # Founded
        return lst
