from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, TimeField, IntegerField, SelectField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class ReservationForm(FlaskForm):
    customer_name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=20)])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    guests = IntegerField('Number of Guests', validators=[DataRequired(), NumberRange(min=1, max=20)])

class MenuItemForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Category', choices=[
        ('appetizers', 'Appetizers'),
        ('main_courses', 'Main Courses'),
        ('desserts', 'Desserts'),
        ('beverages', 'Beverages'),
        ('specials', 'Specials')
    ])
    image_url = StringField('Image URL', validators=[Length(max=255)])
    dietary_info = StringField('Dietary Information', validators=[Length(max=255)])
