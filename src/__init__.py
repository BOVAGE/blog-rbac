from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask_login import LoginManager

load_dotenv()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    db.init_app(app)

    from .models import User
    from .blog import blog
    from .auth import auth


    create_database(app)

    login_manager = LoginManager() # handles session for users 
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        with app.app_context():
            return User.query.get(int(id))

    app.register_blueprint(blog, url_prefix="")
    app.register_blueprint(auth, url_prefix="/auth")
    return app

def create_database(app):
    if not os.path.exists("instance/" + "db.sqlite"):
        with app.app_context():
            db.create_all()
        print("Database created")