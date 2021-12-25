from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security

def create_app():
    app = Flask(__name__)
    #TODO: Secure cookies and session data - Remove in production!!
    app.config['SECRET_KEY'] = 'ThisIsMyKey'

    from .views import views

    app.register_blueprint(views,url_prefix='/')

    return app