
class ModelController:
    template = 'model_view.html'
    model_object_template ='model_object.html'
    url:str
    __models__ = []

    @classmethod
    def register_model_view(self,model):
        if model.__tablename__ not in self.__models__:
            self.__models__.append(model)

    @classmethod 
    def get_models(self):
        print("Список зарегистрированных моделей", self.__models__)
    
    @classmethod
    def get_registred_model_names(self):
        names = [ model.__tablename__ for model in self.__models__]
        return names

    @flask_app.route('/admin/tables/<model_name>/')
    async def __render_model__(model_name,models = __models__, template = template):
        tables = DB.engine.table_names()
        model = [i for i in models if i.__tablename__ == model_name][0]
        q_objects = DB.current_session.query(model).all()
        head,objects = [],[]
        for obj in q_objects:
            obj_dict= {}
            obj_vars = vars(obj)
            obj_dict['id'] = obj_vars['id']
            head.append('id')
            for key, value  in obj_vars.items():
                if key not in ['_sa_instance_state', 'password','id']:
                    obj_dict[key] = value
                    head.append(key)                    
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
        tables = DB.engine.table_names()
        Model = [i for i in models if i.__tablename__ == model_name][0]
        colums = [m for m in Model.__table__.columns]
        model_fields={m.name:m.type for m in colums }
        fields = {}
        for fname, ftype in model_fields.items():
            if ftype.__class__.__name__ == "Integer":
                fields[fname] = "number"
            if ftype.__class__.__name__ == "String":
                fields[fname] = "text"
        
        if request.method == 'POST':
            form_data = request.form
            obj = Model(*[form_data[data] for data in form_data])
            DB.current_session.commit()
        return render_template(model_object_template, tables = tables, model_name = model_name,model_fields = fields)
    @flask_app.route('/admin/tables/<model_name>/<id>',methods=['GET','POST'])
    async def __change__(mode_name,id, model_object_template=model_object_template):
        pass