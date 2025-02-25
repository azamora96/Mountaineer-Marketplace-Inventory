from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User

#from . import db


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                flash("Succesful Log in")
                return redirect(url_for('view.home'))
            else:
                flash("Incorrect Password")
        else:
            flash("Incorrect User")



    return render_template("login.html", boolean=True)

@auth.route("/logout")
def logout():
    return "<p>Logout</p>"

@auth.route("/signup",methods=['GET','POST'])
def signup():
    data = request.form
    return render_template("sign_up.html")