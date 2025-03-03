from flask import Blueprint, render_template
from . import db
from .models import Products, User
from datetime import datetime
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    date_format = "%Y-%m-%d"
    best_by_date = datetime.strptime("2025-02-24", date_format).date()
    expiration_date = datetime.strptime("2025-02-24", date_format).date()
    date_arrived_date = datetime.strptime("2025-02-24", date_format).date()

    test_product = Products.query.filter_by(name="Test Product").first()
    test_user = User.query.filter_by(email="test@western.edu").first()

    if not test_user:
        test_user = User(
            email="test@western.edu",
            password="test"
        )
        db.session.add(test_user)
        db.session.commit()

    if not test_product:
        test_product = Products(
            image="test_image.png",
            name="Test Product",
            tefap="Yes",
            best_by=best_by_date,
            expiration=expiration_date,
            location="Test Location",
            quantity=100,
            date_arrived=date_arrived_date,
        )
        db.session.add(test_product)
        db.session.commit()

    all_products = Products.query.all()

    return render_template("home.html", results=all_products)

@views.route('/edit')
@login_required
def edit():

    return render_template("edit.html")