from flask import render_template, url_for
from src.models import cursor

#--------------departments handler-------------------------------    
def departmentsPrinter():
    
    command = """SELECT {departments}.dept_id, {departments}.dept_name, {departments}.warranty, {departments}.dept_phone, {departments}.dept_manager
    FROM {departments}
    """.format( departments = "departments")
    cursor.execute(command)
    departments_data = cursor.fetchall()
    
    return render_template('departments.html', departments_data = departments_data, URL = url_for('departmentsPrinter'))

#-------------------------------------------------------------------------
def get_message_dept(ID):
    command = """SELECT {departments}.dept_id, {departments}.dept_name, {departments}.warranty, {departments}.dept_phone, {departments}.dept_manager
    FROM {departments} WHERE {departments}.dept_id = {num_id}
    """.format( departments = "departments",  num_id = ID)
    cursor.execute(command)
    departments_data = cursor.fetchall()
    
    return render_template('departmentShower.html', ID = ID, URL = url_for('get_message', ID = ID), departments_data = departments_data)