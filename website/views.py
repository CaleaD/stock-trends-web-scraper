'''
Application blueprint, it stores all the paths to the pages the user will be able to navigate to.
'''
from flask import Blueprint, render_template, request, flash

views = Blueprint('views', __name__)

@views.route('/',methods=['GET','POST'])
def home():
    data = request.form.get('user-query')

    #check if user-query (ticker) is in database/exists for scraping, if not tell it so
    # 1) if in database -> display
    # 2) else if in scraper -> add scraped data to database
    # 3) else -> not found

    # Error handling - flask has MESSAGE FLASHING, usage flash('sth here', category = 'error/success/etc')
    #data = request.form
    if data:
        flash(data, category='success')
    print(data)
    return render_template("home.html")

@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/feed')
def feed():
    return render_template("feed.html")