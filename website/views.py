'''
Application blueprint, it stores all the paths to the pages the user will be able to navigate to.
'''
from flask import Blueprint, render_template, request, flash,json
from flask_sqlalchemy import SQLAlchemy
from .models import Stock
from fin_scraper import FinScraper
from rss_scraper import NewsScraper
import requests

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

@views.route('/',methods=['GET','POST'])
def home():
    data = request.form.get('user-query')

    #q = session.query(Stock.id).filter(Stock.symbol == data.upper())
    if data:
        filtered = filter(data)
        #Scraper Settings
        if isinstance(filtered, list):
            pass
            #TODO: Do it for multiple symbols!
        else:
            exists = db.session.query(db.session.query(Stock).filter_by(symbol=filtered.upper()).exists()).scalar()
            if exists == True:
                print("--- (DB) : Selecting row with symbol and returning to user",filtered,"---")
                #db.select().where(db.c.symbol == filtered.upper())
                #TODO: Get from database!
                pass
            else:
                try:
                    result = FinScraper(filtered).scraper()
                    flash(result, category='success')
                    print("--- (FIN SCRAPER) : Input has been scraped and result added to database ---\n",result)
                    #TODO: Add to database!
                except:
                    flash("Invalid input, please try again. The input should be a stock ticker (e.g: APPL,SBUX,MSFT).", category='error')

    #check if user-query (ticker) is in database/exists for scraping, if not tell it so
    # 1) if in database -> display
    # 2) else if in scraper -> add scraped data to database
    # 3) else -> not found

    # Error handling - flask has MESSAGE FLASHING, usage flash('sth here', category = 'error/success/etc')
    #data = request.form
    return render_template("home.html")

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