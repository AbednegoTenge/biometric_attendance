from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_login import UserMixin

db = SQLAlchemy()

class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(100))
    email:Mapped[str] = mapped_column(String(100), unique=True)
    password:Mapped[str] = mapped_column(String(100))

    attendances = relationship('Attendance', back_populates='user')

    def __init__(self, name, email):
        self.name = name
        self.email = email


class Attendance(UserMixin, db.Model):
    __tablename__ = 'attendance'
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    timestamp:Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    status:Mapped[str] = mapped_column(String(100))

    user = relationship("Users", back_populates="attendances")

Users.attendances = relationship("Attendance", order_by=Attendance.id, back_populates="users")
