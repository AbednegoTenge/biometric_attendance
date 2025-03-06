from flask import Flask, abort
import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from functools import wraps 
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate 

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

db = SQLAlchemy(model_class=Base)
db.init_app(app)

from models import Users, Attendance

migrate = Migrate(app, db )

admin = Admin(app, template_mode='bootstrap3')
admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Attendance, db.session))

@app.route('/')
def home():
    return "Hello, World"


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(404)
        return f(*args, **kwargs)
    return decorated_function


if __name__ == '__main__':
    app.run(debug=True)