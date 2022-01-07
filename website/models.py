from . import db

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    symbol = db.Column(db.String(6), unique=True)
    price = db.Column(db.Numeric(10,2), nullable=True)
    open = db.Column(db.Numeric(10,2), nullable=True)
    close = db.Column(db.Numeric(10,2), nullable=True)
    mcap = db.Column(db.Numeric(10,2), nullable=True)
    volume = db.Column(db.Numeric(10,2), nullable=True)
    dmin = db.Column(db.Numeric(10,2), nullable=True)
    dmax = db.Column(db.Numeric(10,2), nullable=True)
    ymin = db.Column(db.Numeric(10,2), nullable=True)
    ymax = db.Column(db.Numeric(10,2), nullable=True)

