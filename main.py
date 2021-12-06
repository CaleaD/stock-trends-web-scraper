from fin_scraper import FinScraper
from rss_scraper import NewsScraper
import requests
from bs4 import BeautifulSoup
import datetime
import urllib
import yfinance as yf
import matplotlib.pyplot as plt

def plot_price_range(ticker, stock, range):
    '''
    :param ticker: for format use
    :param stock: the yahoo finance stock object
    :param range: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, max and ytd
    :return:
    '''
    stock_dict = stock.history(period=range)
    print(stock_dict['Close'].head())
    plt.figure(figsize=(16, 8))
    plt.plot(stock_dict['Close'], label='Close Price history')
    plt.title(f"{ticker} Market Prices",fontsize=20)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.savefig(f'{ticker}_{range}_prices.png')
    plt.show()

def plot_price_day(ticker, stock):
    '''
    :param ticker: for format use
    :param stock: the yahoo finance stock object
    :return: Timeseries of today's market prices for a stock
    '''
    stock_dict = stock.history(period='1d',interval='1m')
    print(stock_dict['Close'].head())
    plt.figure(figsize=(16, 8))
    plt.plot(stock_dict['Close'], label='Close Price history')
    plt.title(f"{ticker} Market Prices - Date : {datetime.date.today()}",fontsize=20)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.savefig(f'{ticker}_{datetime.date.today()}_prices.png')
    plt.show()

def scraper_lst(tickers):
    '''
    :return: Nested list with market data for multiple stocks
    '''
    stocks = []
    for ticker in tickers:
        scr = FinScraper(ticker)
        stock_values = scr.scraper()
        stocks.append(stock_values)
        del scr
    return stocks

if __name__ == '__main__':
    try:
        ticker = "AAPL"
        tickers = ["AAPL","SBUX","MSFT"]

        ns = NewsScraper(ticker)
        fs = FinScraper(ticker)


        #NEWS DATA
        articles = ns.scraper()
        print(articles)
        ns.save_to_json(articles)
        #ns.filter_json()

        #print(fs.hist_data())
        #print(fs.hist_data2())

        #FINANCIAL DATA
        #TODO: See FinScraper class, method scraper
        print(fs.scraper())
        print(scraper_lst(tickers))


        #YFinance lib + plot testing
        stock = yf.Ticker(ticker)
        #print(stock.history(period='1d', interval='1m'))
        #current_price = stock.history(period='1d')['Close'][0]
        #print(current_price)

        #plot_price_range(ticker,stock,'1mo')
        #plot_price_day(ticker,stock)

    except urllib.error.HTTPError:
        print("HTTP Error 404")
    except Exception as e:
        print(e)

