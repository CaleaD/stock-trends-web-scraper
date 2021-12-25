from fin_scraper import FinScraper
from rss_scraper import NewsScraper
import sqlite3
import datetime
import urllib
import yfinance as yf
import matplotlib.pyplot as plt


''' PLOTTING FUNCTIONS'''
def plot_multiple(tickers):
    '''
    Plots multiple stocks for today.
    :param tickers: a list of all stock symbols to plot
    :return:
    '''
    plt.figure(figsize=(16, 8))
    for symb in tickers:
        stock = yf.Ticker(symb)
        stock_dict = stock.history(period='5y', interval='1mo')
        plt.plot(stock_dict['Close'].bfill(), label=f'{symb}')
    plt.title(f"Market Prices Comparison - 5 Years", fontsize=20)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.grid()
    plt.legend()
    plt.savefig(f'Comparison_prices5y.png')
    plt.show()

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
    plt.plot(stock_dict['Close'], label='Close Price history', color="green")
    plt.title(f"{ticker} Market Prices",fontsize=20)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid()
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
    plt.plot(stock_dict['Close'], label='Close Price history', color="green")
    plt.title(f"{ticker} Market Prices - Date : {datetime.date.today()}",fontsize=20)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.grid()
    plt.savefig(f'{ticker}_{datetime.date.today()}_prices.png')
    plt.show()


''' MANAGE INPUT'''
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

def filter(user_input):
    '''
    :param user_input: can be in the form of a string 'SYMBOL' or 'SYMB1, SYMB2, SYMB3, ...'
    :return: list if it is comma separated, otherwise the same
    '''
    if user_input.find(',')==-1:
        print(user_input)
        return user_input
    else:
        symbols = [x.strip() for x in user_input.split(',')]
        return symbols


''' DATABASE '''
conn = sqlite3.connect('metricshare.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS stock(
            Symbol TEXT,
            Price REAL,
            [Close] REAL,
            MarketCap TEXT,
            Volume INT, #Million
            PER REAL,
            Divident DECIMAL,
            PrimaryEchange TEXT,
            CDP CHAR,
            CEO TEXT,
            Founded DATE,
            HQ TEXT,
            Website TEXT,
            DayMin REAL,
            DayMax REAL,
            YearMin REAL,
            YearMax REAL,
            )''')

# def insert_to_db(data):
#     c.execute('''INSERT INTO stock VALUES)''')


if __name__ == '__main__':
    try:
        #INPUT STOCKS
        ticker = "AAPL"
        tickers_str = "AAPL, SBUX, MSFT"
        tickers = filter(tickers_str)
        #tickers = input("Search for stocks (for multiple stocks separate by comma): ")

        ns = NewsScraper(ticker)

        user_input = input("Search for stocks (for multiple stocks separate by comma): ")
        filtered = filter(user_input)

        #NEWS DATA
        print('---RSS SCRAPER---')
        articles = ns.scraper()
        print(articles)
        ns.save_to_json(articles)
        #ns.filter_json()

        #FINANCIAL DATA
        print('---FIN SCRAPER---')
        #TODO: See FinScraper class, method scraper

        # print(fs.scraper())
        # print(scraper_lst(tickers))

        print("FILTERED DATA:",filtered)
        if isinstance(filtered,list):
            data = scraper_lst(filtered)
            print(data)
            # insert_to_db(data)
            print('Generating plots...\n')
            plot_multiple(filtered)
        else:
            print(FinScraper(filtered).scraper())
            stock = yf.Ticker(filtered) # for plotting
            print('Generating plots...\n')
            print('RANGE PLOT TABLE\n')
            plot_price_range(filtered,stock,'1mo')
            print('\nDAY PRICE PLOT TABLE\n')
            plot_price_day(filtered,stock)
            print('\nDownloading historical data...\n')
            data = FinScraper(filtered).hist_data2()
            # print(FinScraper(filtered).hist_data())
            print(data)
            data.to_csv(f'hist_{filtered}.csv', index = None, header=True)

        #YFinance lib + plot testing
        #print(stock.history(period='1d', interval='1m'))
        #current_price = stock.history(period='1d')['Close'][0]
        #print(current_price)

    except urllib.error.HTTPError:
        print("HTTP Error 404")
    except Exception as e:
        print(e)

