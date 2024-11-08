from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import User, MenuItem, Reservation, Order
from forms import LoginForm, ReservationForm, MenuItemForm
from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    menu_items = MenuItem.query.filter_by(available=True).all()
    categories = sorted(set(item.category for item in menu_items))
    category_icons = {
        'appetizers': 'pie-chart',  # Changed from 'utensils' to valid Feather icon
        'main_courses': 'package',
        'desserts': 'heart',
        'beverages': 'coffee',
        'specials': 'star'
    }
    return render_template('menu.html', 
                         menu_items=menu_items, 
                         categories=categories, 
                         category_icons=category_icons)

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    form = ReservationForm()
    if form.validate_on_submit():
        reservation = Reservation(
            customer_name=form.customer_name.data,
            email=form.email.data,
            phone=form.phone.data,
            date=form.date.data,
            time=form.time.data,
            guests=form.guests.data
        )
        db.session.add(reservation)
        db.session.commit()
        flash('Reservation submitted successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('reservation.html', form=form)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('auth/login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Admin routes
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied.', 'error')
        return redirect(url_for('index'))
    
    menu_items = MenuItem.query.all()
    reservations = Reservation.query.filter(
        Reservation.date >= datetime.today()
    ).order_by(Reservation.date).all()
    customers = User.query.filter_by(is_admin=False).all()
    orders = Order.query.all()
    recent_reservations = Reservation.query.order_by(
        Reservation.created_at.desc()
    ).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         menu_items=menu_items,
                         reservations=reservations,
                         customers=customers,
                         orders=orders,
                         recent_reservations=recent_reservations)

@app.route('/admin/menu', methods=['GET', 'POST'])
@login_required
def admin_menu():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    form = MenuItemForm()
    if form.validate_on_submit():
        menu_item = MenuItem(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category=form.category.data,
            image_url=form.image_url.data,
            dietary_info=form.dietary_info.data
        )
        db.session.add(menu_item)
        db.session.commit()
        flash('Menu item added successfully!', 'success')
        return redirect(url_for('admin_menu'))
    menu_items = MenuItem.query.all()
    return render_template('admin/menu_management.html', form=form, menu_items=menu_items)

@app.route('/admin/reservations')
@login_required
def admin_reservations():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    reservations = Reservation.query.order_by(Reservation.date.desc()).all()
    return render_template('admin/reservations.html', reservations=reservations)

@app.route('/admin/customers')
@login_required
def admin_customers():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin/customers.html', users=users)
