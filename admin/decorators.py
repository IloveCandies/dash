from functools import wraps
from flask_login import login_required, current_user

from admin.controllers import *

def admin_required(func):
    
    @wraps(func)
    def check_admin():
        if current_user.role != "Admin":
            return "403 access denied"
        else:
            func()
    return check_admin
