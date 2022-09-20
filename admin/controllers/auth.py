
from flask import Flask, escape,Blueprint, render_template, redirect, url_for, request,flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,login_user,login_required, current_user
import sqlalchemy 

from main import flask_app
from db.base import *
from admin.controllers.view_controller import ViewController
from admin.decorators import admin_required

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(flask_app)

@login_manager.user_loader
def get_user(ident):
  return User.query.get(int(ident))

@login_manager.user_loader
def load_user(user_id):
    user = DB.current_session.query(User).get(int(user_id))
    return user

@flask_app.route("/")
def flask_main():
    name = request.args.get("name", "World")
    return f"Hello, {escape(name)} from Flask!"

@admin_required
@flask_app.route('/admin/dashboard/')
def admin():
    tables = ViewController.get_registred_model_names()
    return render_template('base.html', tables = tables)

@flask_app.route('/login', methods=['POST','GET'])
def login_post():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = DB.current_session.query(User).filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.',user.password)
            return redirect(url_for('login_post')) 

        login_user(user, remember=remember)
        return redirect(url_for('admin'))
    return render_template('login.html')


@flask_app.route("/signup",methods=['POST','GET'])
def signup_post():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        username = request.form.get('username')
        user = DB.current_session.query(User).filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('signup_post'))
        new_user = User(    name = username ,email = email ,password = generate_password_hash(password, method='sha256'), role = "Admin")
        DB.current_session.add(new_user)
        DB.current_session.commit()
        return redirect(url_for('login_post'))
    return render_template('signup.html')