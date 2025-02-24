from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'you aint getting by me lol'

    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix="/")
    app.register_blueprint(auth,url_prefix="/")
    
    return app

def create_database():
    app = Flask(__name__, static_url_path="/static")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product_db.sqlite'
    db = SQLAlchemy(app)
    app.app_context().push()

    class Products(db.Model):
    primary_id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100))
    name = db.Column(db.String(50))
    tefap = db.Column(db.Boolean)
    best_by = db.Column(db.Date)
    expiration = db.Column(db.Date)
    location = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    date_arrived = db.Column(db.Date)