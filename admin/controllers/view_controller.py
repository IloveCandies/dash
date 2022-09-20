from flask import Flask, escape,Blueprint, render_template, redirect, url_for, request,flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,login_user,login_required, current_user
import sqlalchemy 

from db.base import *
from main import flask_app
from admin.decorators import admin_required


