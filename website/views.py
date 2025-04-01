import os
from flask import Blueprint, render_template, request, url_for, redirect
from . import db
from .models import Products, User
from datetime import datetime
from flask_login import login_user, login_required, logout_user, current_user
from flask import jsonify
from flask_mail import Message
from . import mail

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    all_products = Products.query.all()
    return render_template("home.html", results=all_products)

@views.route('/filter/<string:filter>')
@login_required
def filter(filter):
    sort_column = "name"  
    sort_order = "asc"  

    if filter == "all":
        sort_column="primary_id"
    elif filter == "name_asc":
        sort_column = "name"
    elif filter == "name_desc":
        sort_column = "name"
        sort_order = "desc"
    elif filter == "quantity_asc":
        sort_column = "quantity"
    elif filter == "quantity_desc":
        sort_column = "quantity"
        sort_order = "desc"
    elif filter == "location":
        sort_column="location"
    elif filter == "expiration":
        sort_column="expiration"
    elif filter == "date_arrived":
        sort_column = "date_arrived"
    elif filter =="best_by":
        sort_column="best_by"

    #<option value="all"> All</option>
     #               <option value="name_asc"> Name Ascending</option>
     #               <option value="name_desc"> Name Descending</option>
     #               <option value="quantity_asc"> Quantity Ascending</option>
     #               <option value="quantity_desc"> Quantity Descending</option>
     #               <option value="location"> Location </option>
     #               <option value="expiration"> Expiration </option>
     #               <option value="date_arrived"> Date Arrived </option>
     #               <option value="best_by"> Best by</option>

    if sort_order == "asc":
        filtered_products = Products.query.order_by(getattr(Products, sort_column)).all()
    else:
        filtered_products = Products.query.order_by(getattr(Products, sort_column).desc()).all()


    results = []  

    for product in filtered_products:
   
        product_dict = {
            "primary_id": product.primary_id,
            "name": product.name,
            "date_arrived": product.date_arrived.strftime('%Y-%m-%d') if product.date_arrived else "",
            "tefap": product.tefap,
            "best_by": product.best_by.strftime('%Y-%m-%d') if product.best_by else "",
            "expiration": product.expiration.strftime('%Y-%m-%d') if product.expiration else "",
            "location": product.location,
            "quantity": product.quantity,
            "image": product.image
        }
        results.append(product_dict)


    return jsonify(results=results)  


@views.route('/plus/<int:id>', methods=['POST'])
@login_required
def plus(id):
    product = Products.query.get_or_404(id)

    product.quantity = product.quantity + 1
    db.session.commit()
    return redirect(url_for('views.home')) 

    
@views.route('/minus/<int:id>', methods=['POST'])
@login_required
def minus(id):
    product = Products.query.get_or_404(id)

    if product.quantity > 0:
        product.quantity = product.quantity - 1
    db.session.commit()
    return redirect(url_for('views.home')) 


@views.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    product = Products.query.get_or_404(id)  # Get product ID, found this one line on StackOverflow seems legit

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
@login_required
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
            upload_folder = os.path.join('website','static', 'uploads')
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

@views.route('/delete/<int:item_id>', methods=['DELETE'])
@login_required
def delete_item(item_id):
    product = Products.query.get_or_404(item_id)

    db.session.delete(product)
    db.session.commit()

    msg = Message("Inventory Removed Alert", sender='mountaineer.marketplace.alerts@gmail.com', recipients=["projectkhandro@gmail.com"] )    
    msg.body = product.name + " with expiration of " + product.expiration.strftime("%m-%d-%Y") + " removed from inventory."
    mail.send(msg)
    
    return jsonify({'success': True})


