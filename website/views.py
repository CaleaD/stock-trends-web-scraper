'''
Application blueprint, it stores all the paths to the pages the user will be able to navigate to.
'''
from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/feed')
def feed():
    return render_template("feed.html")