from functools import wraps
from flask import render_template, request, url_for, flash, redirect, session
from src.models import cursor
from src.models import AdvancedSearch

#--------------logged in wrapper------------------------------------------------
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first!", 'danger')
            return redirect(url_for('login'))
    return wrap

#--------------logged out wrapper------------------------------------------------
def logout_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' not in session:
            return f(*args, **kwargs)
        else:
            flash("You are already logged in!", 'danger')
            return redirect(url_for('home'))
    return wrap

#----------------------------Advanced Search function----------------------------------
def AdvSearch():
    form = AdvancedSearch(request.form)

    #command = """ SELECT {departments}.dept_id, {departments}.dept_name 
    #            FROM departments
    #""".format(departments = 'departments')#changed a bit for CHOICES
    #cursor.execute(command)
    #departments = cursor.fetchall()
    command = """ SELECT {departments}.dept_id, {departments}.dept_name 
                    FROM departments
        """.format(departments = 'departments')#changed a bit for CHOICES
    cursor.execute(command)
    departments = cursor.fetchall()

    form.dept_id.choices = form.dept_id.choices + departments 
    
    return render_template('advanced_search.html', URL = url_for('AdvSearch'), form = form)