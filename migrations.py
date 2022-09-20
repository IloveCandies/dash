from werkzeug.security import generate_password_hash
from db.base import *

DB.createall()
DB.createsuperuser(password = generate_password_hash("admin",method='sha256'))
