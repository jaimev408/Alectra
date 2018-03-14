from flask import render_template, request, url_for, flash, redirect, session
from src.models import cursor, conn
from src.models import LoginForm, RegistrationForm, ProductForm, DepartmentForm

#--------------------------------User Tools Function-----------------------------------------------

def user_tools():
    return render_template('user_tools.html', URL = url_for('user_tools'))
    
#--------------------------------Department Create Function-----------------------------------------------
def department_create():
    command  = """ SELECT MAX(dept_id)
    FROM departments
    """
    cursor.execute(command)
    next_id = cursor.fetchone()
    new_id = next_id[0] + 1

    form = DepartmentForm(request.form,csrf_enabled = False)

    if(request.method == 'POST' and form.validate()):
            dept_name   = form.dept_name.data
            warranty    = form.warranty.data
            dept_phone  = int(form.dept_phone.data)
            dept_manager= form.dept_manager.data

            command = """INSERT INTO departments
            (dept_id, dept_name, warranty, dept_phone, dept_manager)
            VALUES
            ('{id}','{name}',{warranty}, '{phone}', '{manager}')
            """.format(id = new_id, name = dept_name, warranty = warranty, phone = dept_phone, manager = dept_manager)

            cursor.execute(command)
            conn.commit()
            
            flash("The department %s with %s as the manager has been created" % (dept_name, dept_manager))
            return redirect(url_for('departmentsPrinter'))#You had the url for completely wrong. Maybe you forgot to change hers?

    if form.errors:
            flash(form.errors, 'danger')

    return render_template('department_create.html', URL = url_for('department_create'), form = form, dept_id = new_id)#forgot to send URl = url_for('product_create'). It's necessary for the title.

#-----------------------Department delete main function--------------------------
def department_delete_main():
    command = """SELECT {departments}.dept_id, {departments}.dept_name, {departments}.warranty, {departments}.dept_phone, {departments}.dept_manager
    FROM {departments}
    """.format( departments = "departments")
    cursor.execute(command)
    departments_data = cursor.fetchall()
    return render_template('departmentDel.html', URL = url_for('department_delete_main'), departments_data = departments_data)

#-----------------------------Department Delete Function----------------------------------------------

def department_delete(key):
    command = """ SELECT *
                    FROM departments
                    WHERE departments.dept_id = {p1}
            """.format(p1 = key)#select whole row of <key>
    cursor.execute(command)
    single_row = cursor.fetchall()   
    dept_name = single_row#gets the name from row 0 column 1

    
    command = """ DELETE FROM departments
                    WHERE departments.dept_id = {p1}
            """.format(p1 = key)

    cursor.execute(command) 
    conn.commit()   
    
    flash('The product %s has been deleted' % (dept_name), 'success')
    return redirect(url_for('department_delete_main'))

#----------------------------Department edit Main function---------------------------
def department_edit_main():
    command = """SELECT {departments}.dept_id, {departments}.dept_name, {departments}.warranty, {departments}.dept_phone, {departments}.dept_manager
    FROM {departments}
    """.format( departments = "departments")
    cursor.execute(command)
    departments_data = cursor.fetchall()
    return render_template('departmentEdit.html', URL = url_for('department_edit_main'), departments_data = departments_data)

#---------------------------Department Edit Function------------------------------

def department_edit(key):
    command = """SELECT * 
                FROM departments
                WHERE dept_id = {p1}
    """.format(p1 = key)
    cursor.execute(command)
    single_department = cursor.fetchall()[0] #gets all the information on the product with id = <key>

    form = DepartmentForm(request.form, csrf_enabled = False, dept_name = single_department[1], warranty = single_department[2],
                        dept_phone = single_department[3], dept_manager = single_department[4])

    if(request.method == 'POST' and form.validate()):
        dept_name   = form.dept_name.data
        warranty    = form.warranty.data
        dept_phone  = form.dept_phone.data
        dept_manager= form.dept_manager.data

        command = """ 
        UPDATE departments 
        SET dept_name = '{name}', warranty = '{warranty}', dept_phone = '{phone}', 
        dept_manager = '{manager}'
        WHERE departments.dept_id = {id}
        """.format(departments = 'departments', id = key, name = dept_name, warranty = warranty, phone = dept_phone, manager = dept_manager)

        cursor.execute(command)
        conn.commit()

        flash('The department %s has been edited.' % (dept_name), 'success')
        return redirect(url_for('department_edit_main'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('department_edit.html', form = form, dept_id = key)#not sure about here

#--------------------------------Product Create Function-----------------------------------------------

def product_create():
    command = """SELECT MAX(prod_id)
                 FROM products
    """  
    cursor.execute(command)
    next_id = cursor.fetchone()
    new_id = next_id[0] + 1

    form = ProductForm(request.form, csrf_enabled = False)#not sure if to have CSRF enabled or not

    command = """ SELECT {departments}.dept_id, {departments}.dept_name 
                FROM departments
    """.format(departments = 'departments')#changed a bit for CHOICES
    cursor.execute(command)
    departments = cursor.fetchall()

    form.dept_id.choices = departments # NOT 100% on what this line does

    if(request.method == 'POST' and form.validate()):
        prod_name   = form.prod_name.data
        dept_id     = form.dept_id.data
        prod_price  = form.prod_price.data
        prod_stock  = form.prod_stock.data
        prod_rating = form.prod_rating.data
        prod_images = form.prod_images.data
        #These have to be if statements because form.shipping.data returns a  bool, which SQLite doesn't accept. It works with 1 and 0
        if (form.shipping.data):
            shipping = 1
        else:
            shipping = 0
        if (form.recycle_fee.data):
            recycle_fee = 1
        else:
            recycle_fee = 0

        command = """ INSERT INTO products
        (prod_id, prod_name, dept_id, prod_price, prod_stock, prod_rating, prod_images, shipping, recycle_fee)
        VALUES
        ('{id}','{name}',{dept}, {price}, {stock},{rating}, '{images}', {ship}, {fee})
        """.format(id = new_id, name = prod_name, dept = dept_id, price = prod_price, stock = prod_stock, rating = prod_rating, images = prod_images, ship = shipping, fee = recycle_fee)#you had shipping = shipping here. It should have been ship=shipping
        
        cursor.execute(command)
        conn.commit()

        flash("The product %s with id %d has been created" % (prod_name, new_id))
        return redirect(url_for('get_message', ID = new_id))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('product_create.html', URL = url_for('product_create'), form = form, prod_id = new_id)

#-------------------------------Product Delete Main Function-----------------------------------------------

def product_delete_main():
    command = """SELECT {products}.prod_id, {products}.prod_name, {products}.dept_id, 
    {products}.prod_price, {products}.prod_stock, {products}.prod_rating, {products}.prod_images, {products}.shipping, {products}.recycle_fee
    FROM {products} JOIN {departments} ON {products}.dept_id = {departments}.dept_id
    """.format(products = 'products', departments = 'departments')
    cursor.execute(command)
    products_data = cursor.fetchall()
    
    return render_template('productDel.html', products_data = products_data, URL = url_for('product_delete_main'))

#-----------------------------Product Delete Function-------------------------------------

def product_delete(key):
    command = """ SELECT *
                    FROM products
                    WHERE products.prod_id = {p1}
            """.format(p1 = key)#select whole row of <key>
    cursor.execute(command)
    single_row = cursor.fetchall()   
    prod_name = single_row#gets the name from row 0 column 1

    
    command = """ DELETE FROM products
                    WHERE products.prod_id = {p1}
            """.format(p1 = key)

    cursor.execute(command) 
    conn.commit()   
    
    flash('The product %s has been deleted' % (prod_name), 'success')
    return redirect(url_for('product_delete_main'))

#-----------------------------Product Edit Main Function-----------------------------------
def product_edit_main():
    command = """SELECT {products}.prod_id, {products}.prod_name, {products}.dept_id, 
    {products}.prod_price, {products}.prod_stock, {products}.prod_rating, {products}.prod_images, {products}.shipping, {products}.recycle_fee
    FROM {products} JOIN {departments} ON {products}.dept_id = {departments}.dept_id
    """.format(products = 'products', departments = 'departments')
    cursor.execute(command)
    products_data = cursor.fetchall()
    
    return render_template('productEdit.html', products_data = products_data, URL = url_for('product_edit_main'))

#----------------------------Product Edit Function-------------------------------------
def product_edit(key):
    command = """SELECT * 
                FROM products
                WHERE prod_id = {p1}
    """.format(p1 = key)
    cursor.execute(command)
    single_product = cursor.fetchall()[0] #gets all the information on the product with id = <key>

    form = ProductForm(request.form, csrf_enabled = False, prod_name = single_product[1], dept_id = single_product[2],
                        prod_price = single_product[3], prod_stock = single_product[4], prod_rating = single_product[5], 
                        prod_images = single_product[6], shipping = single_product[7], recycle_fee = single_product[8])

    command = """SELECT {departments}.dept_id, {departments}.dept_name
                 FROM departments 
    """.format(departments = 'departments') #might run into same problem as prod_create
    cursor.execute(command)
    departments = cursor.fetchall()

    form.dept_id.choices = departments

    if(request.method == 'POST' and form.validate()):
        prod_name   = form.prod_name.data
        dept_id     = form.dept_id.data
        prod_price  = form.prod_price.data
        prod_stock  = form.prod_stock.data
        prod_rating = form.prod_rating.data
        prod_images = form.prod_images.data
        #These have to be if statements because form.shipping.data returns a  bool, which SQLite doesn't accept. It works with 1 and 0
        if (form.shipping.data):
            shipping = 1
        else:
            shipping = 0
        if (form.recycle_fee.data):
            recycle_fee = 1
        else:
            recycle_fee = 0

        command = """ 
        UPDATE products 
        SET prod_name = '{name}', dept_id = '{dept}', prod_price = '{price}', 
        prod_stock = '{stock}', prod_rating = '{rating}', prod_images = '{images}',
         shipping = '{ship}', recycle_fee = '{fee}'
        WHERE products.prod_id = {id}
        """.format(products = 'products', id = key, name = prod_name, dept = dept_id, price = prod_price, stock = prod_stock, rating = prod_rating, images = prod_images, ship = shipping, fee = recycle_fee)
        #not sure if command WHERE should be dept_id or prod_id
        cursor.execute(command)
        conn.commit()

        flash('The product %s has been edited.' % (prod_name), 'success')
        return redirect(url_for('get_message', ID = key))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('product_edit.html', form = form, prod_id = key)

#-------------------------------Register Function-----------------------------------------------

def registerPage():
    command = """ SELECT MAX(user_id) 
					FROM login
					"""
    cursor.execute(command)
    new_id = cursor.fetchone()
    user_id = new_id[0] + 1
    
    form = RegistrationForm(request.form,csrf_enabled=False)
    
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        command = """ SELECT * FROM login WHERE login.username = "{username}" """.format(username =username)
        cursor.execute(command)
        usernametester = cursor.fetchone()
        
        if usernametester != None:
            if username == usernametester[1]:
                flash("That username is already taken, please choose another", 'danger')
                return render_template('registration.html', form = form, URL = url_for('registerPage'))
            
        command = """ INSERT INTO login
                    (user_id, username, email, password)
                    VALUES ({i}, '{u}', '{e}', '{p}')
                    """.format(i = user_id, u = username, e = email, p = password)
        cursor.execute(command)
        conn.commit()
        
        session['logged_in'] = True
        session['username'] = username
        flash('The user %s with ID %d has been created! Logged in!' % (username, user_id), 'success')
        return redirect(url_for('home'))
    
    
    
    if form.errors:
        flash(form.errors, 'danger')
    
    return render_template('registration.html', form = form, URL = url_for('registerPage'))


#-------------------------------Logout Function-----------------------------------------------
def logout():
    session.clear()
    flash("Logged out!", 'success')
    return redirect(url_for('home'))

#-------------------------------Login Function-----------------------------------------------
def login():

    form = LoginForm(request.form)
   
    if (request.method == "POST" and form.validate):
        username = form.username.data
        password = form.password.data
        
        command = """ SELECT * FROM login WHERE login.username = "{username}" """.format(username =username)
        cursor.execute(command)
        usernametester = cursor.fetchone()
        
        if usernametester != None:
            if username == usernametester[1] and password == usernametester[3]:
                session['logged_in'] = True
                session['username'] = username
                flash('Logged in as %s!' % (username), 'success')
                return redirect(url_for('home'))
            else:
                flash('Wrong credentials', 'danger')
                return render_template('login.html', URL = url_for('login'), form = form)
        else:
            flash('Wrong credentials', 'danger')
            return render_template('login.html', URL = url_for('login'), form = form)
        
    return render_template('login.html', URL = url_for('login'), form = form)