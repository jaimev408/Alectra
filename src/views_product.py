from flask import render_template, url_for, request
from src.models import cursor


#--------------products handler---------------------------------  
def productsPrinter():
    command = """SELECT {products}.prod_id, {products}.prod_name, {products}.dept_id, 
    {products}.prod_price, {products}.prod_stock, {products}.prod_rating, {products}.prod_images, {products}.shipping, {products}.recycle_fee
    FROM {products} JOIN {departments} ON {products}.dept_id = {departments}.dept_id
    """.format(products = 'products', departments = 'departments')
    cursor.execute(command)
    products_data = cursor.fetchall()
    
    return render_template("products.html", products_data = products_data, URL = url_for('productsPrinter'))
           
#---------------------Individual Product page handler----------------------------------------------------  
def get_message(ID):
    command = """SELECT {p}.prod_id, {p}.prod_name, {p}.dept_id, {p}.prod_price, 
    {p}.prod_stock, {p}.prod_rating, {p}.prod_images, {p}.shipping, {p}.recycle_fee
    FROM {p} JOIN {d} ON {p}.dept_id = {d}.dept_id
    WHERE {p}.prod_id = {num_id}
    """.format(p = 'products', d = 'departments', num_id = ID)
    
    cursor.execute(command)
    product_data = cursor.fetchall()
    
    return render_template('product.html', ID = ID, URL = url_for('get_message', ID = ID), product_data = product_data)
    
#-------------------------------------------------------------------------------------------------
def searchingFunction():
    if request.method == "POST":
        name = request.form['name']
        condition = ""
        
        if name != None:
            condition += "products.prod_name LIKE '%"+(name)+"%'"
        if condition == "":
            return ('', 204)
           
        else:
            command = """SELECT {products}.prod_id, {products}.prod_name, {products}.dept_id, 
            {products}.prod_price, {products}.prod_stock, {products}.prod_rating, {products}.prod_images, {products}.shipping, {products}.recycle_fee
            FROM {products} JOIN {departments} ON {products}.dept_id = {departments}.dept_id
            WHERE {cond}
            """.format(products = 'products', departments = 'departments', cond = condition)
            
        cursor.execute(command)
        products_data = cursor.fetchall()
        
        return render_template("products.html", products_data = products_data, URL = url_for('searchingFunction'), condition = condition)
            
    if request.method == "GET":
        name = request.args.get('name')
        price = request.args.get('price')
        stock = request.args.get('stock')
        rating = request.args.get('rating')
        shipping = request.args.get('shipping')
        no_recycle = request.args.get('no_recycle_fee')
        department = request.args.get('dept_id')
        price_greater_equal = request.args.get('price_ge')
        price_smaller_equal = request.args.get('price_se')
        rating_greater_equal = request.args.get('prod_rating_ge')
        rating_smaller_equal = request.args.get('prod_rating_se')
        stock_smaller_equal = request.args.get('stock_se')
        stock_greater_equal = request.args.get('stock_ge')
        
        condition = ""
        
        if name != None:
            condition += "products.prod_name LIKE '%"+(name)+"%'"
        if price != None:
            if condition != "":
                condition += " AND "
            condition += "products.prod_price LIKE '%"+str(price)+"%'"
        if stock != None:
            if condition != "":
                condition += " AND "
            condition += "products.prod_stock LIKE '%"+str(stock)+"%'"
        if rating != None:
            if condition != "":
                condition += " AND "
            condition += "products.prod_rating LIKE '%"+str(rating)+"%'"
        if shipping != None:
            if condition != "":
                condition += " AND "
            shipping.lower()
            if shipping == "y" or shipping == "yes" or shipping == "true":
                condition += "products.shipping = 1"
            elif shipping == "n" or shipping == "no" or shipping == "false":
                condition += "products.shipping = 0"
            else:
                condition += ""
        if no_recycle != None:
            if condition != "":
                condition += " AND "
            no_recycle.lower()
            if no_recycle == "n" or no_recycle == "no" or no_recycle == "false":
                condition += "products.recycle_fee = 1"
            elif no_recycle == "y" or no_recycle == "yes" or no_recycle == "true":
                condition += "products.recycle_fee = 0"
            else:
                condition += ""
        if department != '0':
            if condition != "":
                condition += " AND "
            condition += "products.dept_id = " + department
        if price_greater_equal != "":
            if condition != "":
                condition += " AND "
            condition  += "products.prod_price >= " + price_greater_equal
        if price_smaller_equal != "":
            if condition != "":
                condition += " AND "
            condition  += "products.prod_price <= " + price_smaller_equal
        if rating_greater_equal != "":
            if condition != "":
                condition += " AND "
            condition  += "products.prod_rating >= " + rating_greater_equal
        if rating_smaller_equal != "":
            if condition != "":
                condition += " AND "
            #if rating_smaller_equal == "":
             #   condition += ""
            condition  += "products.prod_rating <= " + str(rating_smaller_equal)
        if stock_greater_equal != None:
            if condition != "":
                condition += " AND "
            condition  += "products.prod_stock >= " + stock_greater_equal
        if stock_smaller_equal != None:
            if condition != "":
                condition += " AND "
            condition  += "products.prod_stock <= " + stock_smaller_equal
        
        if condition == "":
            return ('', 204)
           
        else:
            command = """SELECT {products}.prod_id, {products}.prod_name, {products}.dept_id, 
            {products}.prod_price, {products}.prod_stock, {products}.prod_rating, {products}.prod_images, {products}.shipping, {products}.recycle_fee
            FROM {products} JOIN {departments} ON {products}.dept_id = {departments}.dept_id
            WHERE {cond}
            """.format(products = 'products', departments = 'departments', cond = condition)
            
        cursor.execute(command)
        products_data = cursor.fetchall()
        
        return render_template("products.html", products_data = products_data, URL = url_for('searchingFunction'), condition = condition)