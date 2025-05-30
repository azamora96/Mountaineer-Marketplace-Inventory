from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            login_user(user, remember=False)
            return redirect(url_for("views.home"))
        else:
            flash('Invalid username or password.', 'error')  

    return render_template("login.html", boolean=True)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
