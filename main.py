from flask import Flask, escape,Blueprint, render_template, redirect, url_for, request,flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,login_user,login_required, current_user

flask_app = Flask(__name__,template_folder="templates")
flask_app.config['SECRET_KEY'] = '121wqewq232131212232312wdq3213qwq'

from db.base import *
from admin.controllers.auth import *
from admin.controllers.view_controller import *
from admin.views import *

if __name__ == '__main__':
    flask_app.run(debug=True)
