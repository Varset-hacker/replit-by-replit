import os
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

# create the app
app = Flask(__name__)

# setup a secret key, required by sessions
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a secret key"

# configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///restaurant.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

def init_db():
    with app.app_context():
        db.create_all()
        from models import MenuItem
        
        # Only add sample items if table is empty
        if MenuItem.query.count() == 0:
            sample_items = [
                MenuItem(
                    name='Craft Beer',
                    description='Premium locally brewed craft beer',
                    price=7.99,
                    category='beverages',
                    image_url='https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=600&q=80'
                ),
                MenuItem(
                    name='Artisan Pizza',
                    description='Wood-fired pizza with fresh toppings',
                    price=16.99,
                    category='main_courses',
                    image_url='https://images.unsplash.com/photo-1513104890138-7c749659a591?w=600&q=80'
                ),
                MenuItem(
                    name='Fresh Pasta',
                    description='Homemade pasta with signature sauce',
                    price=18.99,
                    category='main_courses',
                    image_url='https://images.unsplash.com/photo-1556760544-74068565f05c?w=600&q=80'
                ),
                MenuItem(
                    name='Signature Cocktail',
                    description='House special mixed drink',
                    price=12.99,
                    category='beverages',
                    image_url='https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=600&q=80'
                )
            ]
            
            for item in sample_items:
                db.session.add(item)
            db.session.commit()

# Import routes after app initialization
with app.app_context():
    import models
    import routes

# Setup error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500
