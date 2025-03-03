import os
from flask import Blueprint, render_template, request, url_for, redirect
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

@views.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    product = Products.query.get_or_404(id)  # Get product ID, found this one line on StackOverflow seems legit
@views.route('/edit')
@login_required
def edit():

    if request.method == 'POST':
        product.name = request.form.get('name')
        product.tefap = request.form.get('TEFAP')
        product.location = request.form.get('location')
        product.quantity = request.form.get('quantity')
        product.best_by = request.form.get('best-by')
        product.expiration = request.form.get('exp')
        product.date_arrived = request.form.get('date-arrived')

        try:
            product.best_by = datetime.strptime(product.best_by, '%Y-%m-%d').date() if product.best_by else None
            product.expiration = datetime.strptime(product.expiration, '%Y-%m-%d').date() if product.expiration else None
            product.date_arrived = datetime.strptime(product.date_arrived, '%Y-%m-%d').date() if product.date_arrived else None
        except ValueError:
            return "Invalid date format", 400

        try:
            product.quantity = int(product.quantity)
        except ValueError:
            return "Invalid quantity", 400

        image = request.files.get('image')
        if image:
            image_filename = image.filename
            upload_folder = os.path.join('static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, image_filename)
            image.save(image_path)
            product.image = image_filename 

        db.session.commit()
        return redirect(url_for('views.home'))

    return render_template('edit.html', product=product)

@views.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        tefap = request.form.get('TEFAP')
        location = request.form.get('location')
        quantity = request.form.get('quantity')
        exp = request.form.get('exp')
        date_arrived = request.form.get('date-arrived')
        best_by = request.form.get('best-by')
        image = request.files.get('image')

        try:
            exp = datetime.strptime(exp, '%Y-%m-%d').date() if exp else None
            date_arrived = datetime.strptime(date_arrived, '%Y-%m-%d').date() if date_arrived else None
            best_by = datetime.strptime(best_by, '%Y-%m-%d').date() if best_by else None
        except ValueError:
            return "Invalid date format", 400

        image_filename = None
        if image:
            image_filename = image.filename
            upload_folder = os.path.join('static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            image_path = os.path.join(upload_folder, image_filename)
            image.save(image_path)

        new_product = Products(
            name=name,
            tefap=tefap,
            location=location,
            quantity=quantity,
            expiration=exp,
            date_arrived=date_arrived,
            best_by=best_by,
            image=image_filename 
        )

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('views.home')) 

    return render_template('add.html')