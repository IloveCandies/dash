
from flask import Flask, escape,Blueprint, render_template, redirect, url_for, request,flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager,login_user,login_required, current_user
import sqlalchemy 

from db.base import *
from main import flask_app
from admin.decorators import admin_required

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(flask_app)

### Перенести в отдельный модуль ###

class BaseViev:
    template = 'model_view.html'
    model_object_template ='model_object.html'
    url:str
    __models__ = []

    @classmethod
    def register_model(self,model):
        if model.__tablename__ not in self.__models__:
            self.__models__.append(model)

    @classmethod 
    def get_models(self):
        print("Список зарегистрированных моделей", self.__models__)

    @flask_app.route('/admin/tables/<model_name>/')
    def __render_model__(model_name,models = __models__, template = template):
        tables = DB.engine.table_names()
        model = [i for i in models if i.__tablename__ == model_name][0]
        q_objects = DB.current_session.query(model).all()
        head = [m.key for m in model.__table__.columns if m not in ['_sa_instance_state', 'password']]
        objects = []
        for obj in q_objects:
            obj_vars = vars(obj)
            obj_dict = { model_key: model_value for model_key, model_value 
                         in obj_vars.items() if model_key not in ['_sa_instance_state', 'password']
                    } 
            objects.append(obj_dict)
        return render_template(template, tables = tables, model_name = model_name, head = head, objects = objects)

    @flask_app.route('/admin/tables/<model_name>/delete', methods=['GET', 'POST'])
    async def __delete__(model_name, models = __models__):
        model = [i for i in models if i.__tablename__ == model_name][0]
        q_objects = DB.current_session.query(model).all()
        if request.method == 'POST': 
            list_on_del = request.form.getlist('checkbox')
            for item in list_on_del:
               query =  sqlalchemy.delete(model).where(model.id == item)
               DB.current_session.execute(query)
               DB.current_session.commit()
                       
            return redirect('/admin/tables/'+ model_name)

    @flask_app.route('/admin/tables/<model_name>/create',methods=['GET','POST'])
    async def __create__(model_name,models = __models__, model_object_template=model_object_template):
        model = [i for i in models if i.__tablename__ == model_name][0]
        colums = [m for m in model.__table__.columns]
        names={m.name:m.type for m in colums }
        
        print(names) 
        if request.method == 'POST':
            DB.current_session.commit()
        return render_template(model_object_template, model_name = model_name)


BaseViev().register_model(User)
BaseViev().get_models()
###################################################################

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
    tables = DB.engine.table_names()
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