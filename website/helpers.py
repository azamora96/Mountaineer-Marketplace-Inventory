from . import db, app, mail
from flask_mail import Message
from datetime import datetime, timedelta
import threading

def send_email(product, subject):
    with app.app_context():
        try:
            product = db.session.merge(product)
            
            msg = Message(subject, sender='mountaineer.marketplace.alerts@gmail.com', recipients=["alec.zamora@western.edu"])

            if subject == "Low Stock Alert":
                if(product.quantity == 1):
                    msg.body = f"{product.name} with expiration of {product.expiration.strftime('%m-%d-%Y')} is low in stock, there is {product.quantity} left."
                else:
                    msg.body = f"{product.name} with expiration of {product.expiration.strftime('%m-%d-%Y')} is low in stock, there are {product.quantity} left."
            elif subject == "Inventory Removed Alert":
                msg.body = f"{product.name} with expiration of {product.expiration.strftime('%m-%d-%Y')} removed from inventory."
            elif subject == "Item Expiring Soon":
                msg.body = f"{product.name} is expiring within a month. It's expiration is {product.expiration.strftime('%m-%d-%Y')}."
            mail.send(msg) 

        except Exception as e:
            print(e)

def send_expiring_email(products, subject):
    with app.app_context():
        try:
            msg = Message(subject, sender='mountaineer.marketplace.alerts@gmail.com', recipients=["alec.zamora@western.edu"])
        
            email_body = "The following items are expiring within 31 days:\n\n"
            
            for product in products:
                email_body += f"{product.name} - Expiration Date: {product.expiration.strftime('%m-%d-%Y')}\n"

            msg.body = email_body

            mail.send(msg) 

        except Exception as e:
            print(e)
        
def expiring_check(all_products):
    expiring_products = []
    current_date = datetime.today().date()
    
    for product in all_products:
        expiration_date = product.expiration
        days_left = (expiration_date - current_date).days
        if 0 <= days_left <= 31:
            expiring_products.append(product)

    if expiring_products:
        threading.Thread(target=send_expiring_email, args=(expiring_products, "Items Expiring Soon")).start()