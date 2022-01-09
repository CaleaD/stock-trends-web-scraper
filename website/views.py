'''
Application blueprint, it stores all the paths to the pages the user will be able to navigate to.
'''
from flask import Blueprint, render_template, request, flash,json
from flask_sqlalchemy import SQLAlchemy
from .models import Stock
import pandas as pd
from fin_scraper import FinScraper
from rss_scraper import NewsScraper
import requests, io, base64, datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import yfinance as yf

views = Blueprint('views', __name__)
db = SQLAlchemy()

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


def plot_price_day(ticker, stock):
    '''
    :param ticker: for format use
    :param stock: the yahoo finance stock object
    :return: Timeseries of today's market prices for a stock
    '''
    stock_dict = stock.history(period='1d',interval='1m')
    print(stock_dict['Close'].head())
    fig = plt.figure(figsize=(16, 8))
    plt.plot(stock_dict['Close'], label='Close Price history', color="green")
    plt.title(f"{ticker} Market Prices - Date : {datetime.date.today()}",fontsize=20)
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
    #TODO: Delete saved images
    data = request.form.get('user-query')
    result = None
    image = None
    csv = None
    #q = session.query(Stock.id).filter(Stock.symbol == data.upper())
    if data:
        filtered = filter(data)
        #Scraper Settings
        if isinstance(filtered, list):
            pass
            #TODO: Do it for multiple symbols!
        else:
            try:
                fs = FinScraper(filtered)
                result = fs.scraper()
                print("--- (FIN SCRAPER) : Input has been scraped and result displayed ---\n",result)
                stock = yf.Ticker(filtered)
                image = plot_price_day(filtered, stock)
                print("--- (TIME SERIES) : Plot has been generated ---\n")
                history = fs.hist_data()
                print(data)
                history.to_csv(f'hist_{filtered}.csv', index = None, header=True)
                print("--- (HISTORICAL DATA) : History saved to csv and sent to HTML ---\n")
                flash("Success! See below for results.", category='success')
                #TODO: Add to database + date!
            except:
                flash("Invalid input, please try again. The input should be a stock ticker (e.g: APPL,SBUX,MSFT).", category='error')

    # Error handling - flask has MESSAGE FLASHING, usage flash('sth here', category = 'error/success/etc')
    #data = request.form
    return render_template("home.html",result = result,img = image)

@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/feed')
def feed():
    # Generating json file
    # ns = NewsScraper('ticker') #TODO: this is not how classes should work! Change it!
    # print('--- RSS SCRAPER : Jsonifying scraped results ---')
    # articles = ns.scraper()
    # print(articles)
    # ns.save_to_json(articles)
    #
    # with open('./articles.json', 'r') as file:
    #     data = file.read()

    #return render_template("feed.html",title="Feed",jsonfile=json.dumps(data))
    data = json.load(open('./articles.json'))
    return render_template('feed.html', data=data)