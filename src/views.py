from flask import render_template, url_for
from src import app

import src.views_department as vd
import src.views_product as vp
import src.views_option_misc as vom
import src.views_user_tools as vut

#Injector for form NavBarSearchForm in case we want to use WRForms for validation in the navbar search
#@app.context_processor
#def inject_searchForm():
#    formNav = NavBarSearchForm(request.form)
#        
#    return dict (formNav = formNav)

#--------------Home Handler-----------------------------------------------
@app.route('/')
@app.route('/homepage')
def home():
    return render_template('home.html', URL= url_for('home'))

@app.route('/contact')
def contact():
    return render_template('contact.html', URL = url_for('contact'))

#--------------Tools Handler-----------------------------------------------

@app.route('/user_tools')
@vom.login_required
def user_tools():
    return (vut.user_tools())


#----------------------------Advanced Search Handler----------------------------------
@app.route('/advanced_search', methods = ['GET', 'POST'])
def AdvSearch():
    return (vom.AdvSearch())


#---------------------------------Register Page Handler---------------------------------------------
@app.route('/register', methods = ['GET', 'POST'])
@vom.logout_required
def registerPage():
    return (vut.registerPage())

#---------------------Logout Handler--------------------------------
@app.route('/logout')
@vom.login_required
def logout():
    return (vut.logout())
#---------------------Login Handler--------------------------------

@app.route('/login', methods = ['GET', 'POST'])
@vom.logout_required
def login():
    return (vut.login())

#---------------------Error Handlers--------------------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', errorType = 404)

@app.errorhandler(500)
def page_not_recognized(e):
    return render_template('error.html', errorType = 500)

#--------------departments handler-------------------------------    
@app.route('/departments')
def departmentsPrinter():
    
    return (vd.departmentsPrinter())

#-----------Departments ------------------------------
@app.route('/departments/<ID>')
def get_message_dept(ID):
    return (vd.get_message_dept(ID))


#--------------Department Create Handler-----------------------------------------------
@app.route('/department_create', methods = ['GET', 'POST'])
@vom.login_required
def department_create():
    return (vut.department_create())

#--------------Department Delete Main Handler
@app.route('/department_delete')
@vom.login_required
def department_delete_main():
    return (vut.department_delete_main())
#--------------Department Delete Handler-------------------------------------------

@app.route('/department_delete/<key>', methods = ['GET', 'POST'])
@vom.login_required
def department_delete(key):
    return vut.department_delete(key)

#-----------------Department edit Main handler--------------

@app.route('/department_edit')
@vom.login_required
def department_edit_main():
    return vut.department_edit_main()

#----------------Department Edit Handler--------------------

@app.route('/department_edit/<key>', methods = ['GET', 'POST'])
@vom.login_required
def department_edit(key):
    return vut.department_edit(key)

#--------------products handler--------------------------------- 
 
@app.route('/products')
def productsPrinter():
    return vp.productsPrinter()

#--------------------------------Product Create Handler-----------------------------------------------
@app.route('/product_create', methods = ['GET', 'POST'])
@vom.login_required
def product_create():
    return (vut.product_create())

#--------------Product delete Main Handler-----------------------------------------------
@app.route('/product_delete')
@vom.login_required
def product_delete_main():
    return (vut.product_delete_main())

#--------------product delete handler---------------------------------  

@app.route('/product_delete/<key>', methods = ['GET', 'POST'])
@vom.login_required
def product_delete(key):
    return vut.product_delete(key)

#-----------------Product edit Main Handler-------------------

@app.route('/product_edit')
@vom.login_required
def product_edit_main():
    return (vut.product_edit_main())

#-----------------Product edit handler--------------------

@app.route('/product_edit/<key>', methods=['GET', 'POST'])
@vom.login_required
def product_edit(key):
    return vut.product_edit(key)

#-------------------------Individual Product Page Handler------------------------------------------------                

@app.route('/products/<ID>')
def get_message(ID):
    
    return vp.get_message(ID)

#-------------------------------------------------------------------------------------------------
@app.route('/products-search', methods = ['GET', 'POST'])
def searchingFunction():
    return vp.searchingFunction()