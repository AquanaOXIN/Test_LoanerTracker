from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "loaner.db"

def create_app():
    app = Flask(__name__) # Initialize Flask
    app.config['SECRET_KEY'] = 'T1S1SH20SEC6ET'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # same folder level where the current file is in
    db.init_app(app)

    # import the blueprints
    from .views import views 
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from . import models

    with app.app_context():
        db.create_all()

    return app
