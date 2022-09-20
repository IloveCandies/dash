# представления для моделей базы данных
from admin.view_controller import ViewController
from db.base import *

ViewController.register_model_view(User)
ViewController.get_models()