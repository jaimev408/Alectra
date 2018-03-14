import wtforms
from wtforms import Form, TextField, PasswordField, BooleanField, SelectField, DecimalField, IntegerField
from wtforms.validators import InputRequired, Email, Length, EqualTo, NumberRange
from decimal import Decimal
import sqlite3

sqlite_file = '/home/lalin90/alectraMinePRIME/electronics.db'
conn = sqlite3.connect(sqlite_file)
cursor = conn.cursor()

#form for NavBarSearchForm. Obselete for now since we did the navbar search bar just with html
#class NavBarSearchForm(Form):
#    name_search = TextField(validators = [Length(min = 1)])

class AdvancedSearch(Form):
    name = TextField(label = "Product Name", validators = [InputRequired()])
    shipping 	= BooleanField(label = 'Free-Shipping?')
    no_recycle_fee = BooleanField(label = 'No Recycle-Fee?')
    dept_id   	= SelectField(label  = 'Department?', choices = [(0, 'All Categories')], validators = [InputRequired()], coerce = int)
    prod_rating_ge = DecimalField(label = "Lowest Rating?", validators = [InputRequired(), NumberRange(min = Decimal('0.0'), max = Decimal('5.0'))])
    prod_rating_se = DecimalField(label = "Highest Rating?", validators = [InputRequired(), NumberRange(min = Decimal('0.0'), max = Decimal('5.0'))])
    price_ge = DecimalField(label = 'Lowes Price?', validators = [InputRequired(), NumberRange(min =Decimal('0.0'))])
    price_se = DecimalField(label = 'Highest Price?', validators = [InputRequired()])

class ProductForm(Form):
	prod_name 	= TextField(label    = 'Name         ', validators = [InputRequired()])
	dept_id   	= SelectField(label  = 'Department   ', validators = [InputRequired()], coerce = int)#not sure what this does checking to see if it works
	prod_price 	= DecimalField(label = 'Price        ', validators = [InputRequired(), NumberRange(min =Decimal('0.01'))])
	prod_stock 	= IntegerField(label = 'Stock        ', validators = [InputRequired()])
	prod_rating = DecimalField(label = 'Rating       ', validators = [InputRequired(), NumberRange(max = Decimal('5.0'))])#not sure about setting max
	prod_images = TextField(label 	 = 'Image URL    ', validators = [InputRequired()])
	shipping 	= BooleanField(label = 'Free-Shipping')
	recycle_fee = BooleanField(label = 'Recycle-Fee  ')  #took out InputRequired() validators for shipping and recycle, since you could only have them be true with it.


class RegistrationForm(Form):
    username = TextField(
		label = 'username',
		validators = [InputRequired(), Length(min = 6, max = 15)])
    email = TextField(
		label = 'email',
		validators = [InputRequired(), Length(min = 6, max = 50), Email(message = "Must be a valid email!")])
    password = PasswordField(
		label = 'password',
		validators = [InputRequired(), Length(min = 5, max = 10), EqualTo('confirm', message = "Passwords must match!")])
    confirm = PasswordField(
		label = 'repeatedPassword')
    TOS = BooleanField(
		label = 'I accept the Terms of Service and to give this project an A if I was grading it',
		validators = [InputRequired()])

class DepartmentForm(Form):
	dept_name    = TextField(label = 'Name', validators = [InputRequired()])
	warranty   	 = IntegerField(label = 'Length of Warranty(yr)', validators = [InputRequired(), NumberRange(max = 6)])#Not sure about this line
	dept_phone 	 = TextField(label = 'Department Phone Number', validators = [InputRequired()])# HAVE to CHECK how to restrict this
	dept_manager = TextField(label = 'Manager', validators = [InputRequired()])

class LoginForm(Form):
	username = TextField(
		label = 'username',
		validators = [InputRequired()])
	password = PasswordField(
		label = 'password',
		validators = [InputRequired()])
