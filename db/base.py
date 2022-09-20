from sqlalchemy import create_engine
from sqlalchemy.orm import registry, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData,Table, Column
from sqlalchemy.types import Boolean, String, Integer
from flask_login import UserMixin

class Database:
    engine = create_engine("sqlite:///example.db",connect_args={"check_same_thread": False},)
    session = sessionmaker(bind = engine)
    base = declarative_base()
    metadata = MetaData
    #thread-local session
    current_session = scoped_session(session)

    @classmethod
    def createall(self):
        self.base.metadata.create_all(self.engine)

    @classmethod
    def createsuperuser(self,name:str = "admin",email:str = "admin@admin.com", password = "admin"):
        role = "Admin"
        user = User(name,email,password,role)
        user.is_active = True
        self.current_session.add(user) 
        self.current_session.commit()
    
    @classmethod
    def get_table_names(self):
        return [key for key in DB.base.registry._class_registry.values]

    @classmethod
    def get_class_by_tablename(self,tablename):
        for cl in self.base.registry._class_registry.values():
            if hasattr(cl, '__tablename__') and cl.__tablename__ == tablename:
                return cl    

DB = Database()
#(UserMixin,DB.base) for flask.login


class User(UserMixin,DB.base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String) 
    role = Column(String)
    is_active = Column(Boolean)

    def __init__(self,id:int, name:str,email:str,password:str,role:str):
        self.name,self.email,self.password,self.role  = name,email,password,role
    

