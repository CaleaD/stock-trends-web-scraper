'''
Application blueprint, it stores all the paths to the pages the user will be able to navigate to.
'''
from flask import Blueprint, render_template, request, flash, json, send_file, abort
from flask_sqlalchemy import SQLAlchemy
from .models import Stock
import pandas as pd
from fin_scraper import FinScraper
from rss_scraper import NewsScraper
import requests, io, base64, datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import yfinance as yf
import os

views = Blueprint('views', __name__)
db = SQLAlchemy()
path = "C:\\Users\\dorac\\OneDrive\\Desktop\\Anul 3\\Web Technologies\\Scraper"

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

def plot_multiple(tickers):
    '''
    Plots multiple stocks for today.
    :param tickers: a list of all stock symbols to plot
    :return:
    '''
    fig = plt.figure(figsize=(16, 8))
    for symb in tickers:
        stock = yf.Ticker(symb[0])
        stock_dict = stock.history(period='5y', interval='1mo')
        plt.plot(stock_dict['Close'].bfill(), label=f'{symb}')
    plt.title(f"Market Prices Comparison - 5 Years", fontsize=20)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.grid()
    plt.legend()
    # Plot to png
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    # Encode img to base64 string
    png = "data:image/png;base64,"
    png += base64.b64encode(pngImage.getvalue()).decode('utf8')

    return png

def plot_price_day(ticker, stock):
    '''
    :param ticker: for format use
    :param stock: the yahoo finance stock object
    :return: Timeseries of today's market prices for a stock
    '''
    stock_dict = stock.history(period='1d',interval='1m')
    #print(stock_dict['Close'].head())

    fig = plt.figure(figsize=(16, 8))
    plt.plot(stock_dict['Close'], label='Close Price history', color="green")
    plt.title(f"{ticker.upper()} Market Prices - Date : {datetime.date.today()}",fontsize=20)
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.grid()
    # plt.savefig(f'/static/images/{ticker}_{datetime.date.today()}_prices.png')
    # Plot to png
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    # Encode img to base64 string
    png = "data:image/png;base64,"
    png+= base64.b64encode(pngImage.getvalue()).decode('utf8')

    return png


@views.route('/',methods=['GET','POST'])
def home():
    data = request.form.get('user-query')
    result = None
    image = None
    multiple = True
    yaxis = []
    if data:
        filtered = filter(data)
        if isinstance(filtered, list):
            try:
                multiple = True
                result = scraper_lst(filtered)
                print('--- (TIME SERIES) : Plot has been generated ---\n')
                image = plot_multiple(filtered)
                flash("Success! See below for results.", category='success')
            except:
                flash("Invalid input, please try again. The input should either be one stock ticker/name or multiple (separate them by commas).(e.g: APPL,SBUX,MSFT)", category='error')
        else:
            try:
                multiple = False
                fs = FinScraper(filtered)
                result = fs.scraper()
                print("--- (FIN SCRAPER) : Input has been scraped and result displayed ---\n",result)
                stock = yf.Ticker(result[0])
                # stock_dict = stock.history(period='1d', interval='1m')
                # yaxis = stock_dict['Close'].bfill().tolist()
                image = plot_price_day(filtered, stock)
                print("--- (TIME SERIES) : Plot has been generated ---\n")
                #history = fs.hist_data(result[0])
                history = stock.history(period='1d',interval='1m')
                print(data)
                history.to_csv(os.path.join(path, r'hist.csv'), index = None, header=True)
                print("--- (HISTORICAL DATA) : History saved to csv and sent to HTML ---\n")
                flash("Success! See below for results.", category='success')
            except:
                flash("Invalid input, please try again. The input should either be one stock ticker/name or multiple (separate them by commas).(e.g: APPL,SBUX,MSFT)", category='error')

    return render_template("home.html",result = result,img = image,multiple=multiple, yaxis=yaxis)

@views.route("/download")
def download_file():
    return send_file(
        os.path.join(path, r'hist.csv'),
        mimetype='text/csv',
        attachment_filename='hist.csv',
        as_attachment=True)


@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/feed')
def feed():
    ns = NewsScraper('ticker')
    print('--- RSS SCRAPER : Jsonifying scraped results ---')
    articles = ns.scraper()
    print(articles)
    ns.save_to_json(articles)
    data = json.load(open('./articles.json'))
    return render_template('feed.html', data=data)