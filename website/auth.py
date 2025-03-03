from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .models import User
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            login_user(user, remember=False)
            return redirect(url_for("views.home"))

    return render_template("login.html", boolean=True)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/signup",methods=['GET','POST'])
def signup():
    data = request.form
    return render_template("sign_up.html")