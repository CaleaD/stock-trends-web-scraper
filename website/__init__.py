from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from os import path

db = SQLAlchemy()
DB_NAME = "metricshare.db"

def create_db(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("The database has been created.")


def create_app():
    app = Flask(__name__)
    #TODO: Secure cookies and session data - Remove in production!!
    app.config['SECRET_KEY'] = 'ThisIsMyKey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views

    app.register_blueprint(views,url_prefix='/')

    from .models import Stock

    create_db(app)

    return app