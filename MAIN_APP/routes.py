from MAIN_APP import app, db
from flask import render_template, url_for, flash, redirect, request
from MAIN_APP.forms import Register_form, Login_form, AddItem, Delete_Form, Edit_Form
from MAIN_APP.models import User, TodoList
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from sqlalchemy import desc
from sqlalchemy.sql.functions import current_timestamp


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = Login_form()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success you logged in as {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))

        else:
            flash(f'Username and Password do not match!', category='danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = Register_form()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'You logged in as {user_to_create.username}', category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error creating your account: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/todo', methods=['GET', 'POST'])
@login_required
def todo_page():
    delete_form = Delete_Form()
    edit_form = Edit_Form()

    if request.method == 'POST':
        # Logic for deletion of activity
        delete_item = request.form.get('delete_item')
        d_item_obj = TodoList.query.filter_by(id=delete_item).first()
        if d_item_obj:
            d_item_obj.delete_list_item()
            flash(f'The list item {d_item_obj.title} is deleted', category='info')

        edit_item = request.form.get('edit_item')
        e_item_obj = TodoList.query.filter_by(id=edit_item).first()
        update_string = edit_form.text.data
        if e_item_obj:
            e_item_obj.update_activity(update_string)
            flash('Activity Updated', category='info')

        return redirect(url_for('todo_page'))

    if request.method == 'GET':
        user_data = TodoList.query.filter_by(owned_user=current_user.id).order_by(desc(TodoList.date_created)).all()
        return render_template('todo.html', user_data=user_data, datetime=datetime, delete_form=delete_form,
                               edit_form=edit_form)


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash('You have been logged out', category='info')
    return redirect(url_for('home_page'))


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_item_page():
    form = AddItem()
    if request.method == 'POST':
        if form.validate_on_submit():
            item_to_add = TodoList(title=form.title.data,
                                   description=form.description.data,
                                   owned_user=current_user.id,
                                   date_created=current_timestamp())
            db.session.add(item_to_add)
            db.session.commit()
            flash('Your activity is added to Your List!', category='success')
            return redirect(url_for('add_item_page'))
        else:
            flash('There was some problem committing please try again!', category='danger')
    if request.method == 'GET':
        return render_template('add_item.html', form=form)
