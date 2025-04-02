from . import db
from flask_login import UserMixin

class Products(db.Model):
    primary_id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100))
    name = db.Column(db.String(50))
    tefap = db.Column(db.String(5))
    best_by = db.Column(db.Date)
    expiration = db.Column(db.Date)
    location = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    date_arrived = db.Column(db.Date)
    alert_num = db.Column(db.Integer)
    low_on_stock = db.Column(db.Boolean, default=False)
    past_best_by = db.Column(db.String(20))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))