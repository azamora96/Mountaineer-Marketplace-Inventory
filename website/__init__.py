from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message

db = SQLAlchemy()
mail = Mail()
app = Flask(__name__)

def create_app():

    #DATABASE CONFIGURATIONS
    app.config['SECRET_KEY'] = 'you aint getting by me lol'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product_db.sqlite'

    #EMAIL CONFIGURATIONS
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'mountaineer.marketplace.alerts@gmail.com'
    app.config['MAIL_PASSWORD'] = 'lyvt dkrh nkip cmdh'
    app.config['MAIL_USE_SSL'] = True


    mail.init_app(app)
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    with app.app_context():
        db.create_all()

    from .models import User 

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app