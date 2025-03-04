from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from flask_login import UserMixin
from main import app

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)
migrate = Migrate(app, db)

class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(100))
    email:Mapped[str] = mapped_column(String(100), unique=True)
    password:Mapped[str] = mapped_column(String(100))

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password


class Attendance(UserMixin, db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    timestamp:Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    status:Mapped[str] = mapped_column(String(100))

    user = relationship("Users", back_populates="attendances")

Users.attendances = relationship("Attendance", order_by=Attendance.id, backpoulates="users")