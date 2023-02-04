from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from . import db


# Database models and relationship
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(50))
    cardType = db.Column(db.String(50))
    cardholder = db.Column(db.String(50))
    valid = db.Column(db.String(5))
    cardnumber = db.Column(db.String(16))


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    empname = db.Column(db.String(50))
    fname = db.Column(db.String(50))
    tel = db.Column(db.String(50))
    emailemp = db.Column(db.String(150), unique=True)
    bookings = relationship("Booking", back_populates="employee")


class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hotelname = db.Column(db.String(150))
    street = db.Column(db.String(150))
    zip = db.Column(db.String(10))
    place = db.Column(db.String(50))
    tel = db.Column(db.String(50))
    fax = db.Column(db.String(50))
    email = db.Column(db.String(150), unique=True)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ed = db.Column(db.String(150))
    hn = db.Column(db.String(150))
    checkin = db.Column(db.DateTime)
    checkout = db.Column(db.DateTime)
    price = db.Column(db.String(50))
    art = db.Column(db.String(50))
    bookDate = db.Column(db.DateTime)
    employee_id = db.Column(db.Integer, ForeignKey("employee.id"))
    employee = relationship("Employee", back_populates="bookings")
