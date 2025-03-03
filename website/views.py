import os
from flask import Blueprint, render_template, request, url_for, redirect
from . import db
from .models import Products
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/')
def home():
    all_products = Products.query.all()
    return render_template("home.html", results=all_products)

@views.route('/edit')
def edit():
    return render_template("edit.html")

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

        new_products = Products.query.all()
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('views.home', results=new_products)) 

    return render_template('add.html')