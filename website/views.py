import os
import threading
import pandas as pd
from flask import Blueprint, render_template, request, url_for, redirect, session, send_file
from . import db, app, mail
from .models import Products, User
from datetime import datetime, timedelta
from .helpers import expiring_check, send_email
from dateutil.relativedelta import relativedelta
from flask_login import login_user, login_required, logout_user, current_user
from flask import jsonify
from flask_mail import Message
from dateutil.relativedelta import relativedelta
from io import BytesIO
from flask import Response
import csv
from io import StringIO


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    all_products = Products.query.all()
    
    expiring_check(all_products)

    return render_template("home.html", results=all_products)


@app.route('/search')
@login_required
def search():
    query = request.args.get('q', '').strip().lower()
    
    results = Products.query.filter(Products.name.ilike(f"%{query}%")).all()
    
    results_json = []
    for item in results:
        results_json.append({
            "primary_id": item.primary_id,
            "image": item.image,
            "name": item.name,
            "date_arrived": item.date_arrived.strftime('%m-%d-%Y') if item.date_arrived else '',
            "tefap": item.tefap,
            "best_by": item.best_by.strftime('%m-%d-%Y') if item.best_by else '',
            "expiration": item.expiration.strftime('%m-%d-%Y') if item.expiration else '',
            "location": item.location,
            "quantity": item.quantity,
        })

    return jsonify(results=results_json)



@views.route("/export")
@login_required
def export():
    all_products = Products.query.all()

    output = StringIO()
    writer = csv.writer(output)

    selected_columns = ["name", "tefap", "best_by", "expiration", "location", "quantity", "date_arrived", "low_on_stock"]

    if all_products:
        writer.writerow(selected_columns)

        for product in all_products:
            writer.writerow([getattr(product, col) for col in selected_columns])

    output.seek(0)

    return Response(
        output,
        mimetype='text/csv',
        headers={"Content-Disposition": "attachment;filename=data.csv"}
    )



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
            "date_arrived": product.date_arrived.strftime('%m-%d-%Y') if product.date_arrived else "",
            "tefap": product.tefap,
            "best_by": product.best_by.strftime('%m-%d-%Y') if product.best_by else "",
            "expiration": product.expiration.strftime('%m-%d-%Y') if product.expiration else "",
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

    new_quantity = product.quantity + 1
    product.quantity = new_quantity
    db.session.commit()
    return redirect(url_for('views.home')) 

    
@views.route('/minus/<int:id>', methods=['POST'])
@login_required
def minus(id):
    product = Products.query.get_or_404(id)

    if product.quantity > 0:
        new_quantity = product.quantity - 1
        product.quantity = new_quantity

        if(new_quantity == product.alert_num):
            product.low_on_stock = True
            threading.Thread(target=send_email, args=(product, "Low Stock Alert")).start()


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
        product.alert_num = request.form.get('alertNum')
        product.past_best_by = request.form.get('past_best_by')

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
            upload_folder = os.path.join('website', 'static', 'uploads')
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
        past_best_by = request.form.get('past_best_by')
        image = request.files.get('image')
        alert_num = request.form.get('alertNum')

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
            image=image_filename,
            alert_num=alert_num,
            past_best_by = past_best_by
        )

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('views.home')) 

    return render_template('add.html')

@views.route('/delete/<int:item_id>', methods=['DELETE'])
@login_required
def delete_item(item_id):
    product = Products.query.get_or_404(item_id)

    threading.Thread(target=send_email, args=(product, "Inventory Removed Alert")).start()
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'success': True})





