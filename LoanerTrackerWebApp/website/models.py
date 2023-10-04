from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

### TO DO --- Separate Device database and Loaner Sign-out sheet Database

# Table for Device themselves information
class Device(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    asset_tag = db.Column(db.Integer, unique=True)
    device_type = db.Column(db.String(150))
    device_status = db.Column(db.String(150))
    note = db.Column(db.String(10000))
    records = db.relationship("Record")

# Table for Loaner Sign-out records
class Record(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    asset_tag = db.Column(db.Integer, db.ForeignKey('device.asset_tag'))
    ticket_number = db.Column(db.String(150))
    tech_name = db.Column(db.String(150), db.ForeignKey('technician.name'))
    out_date = db.Column(db.DateTime(timezone=True), default=func.now())
    note = db.Column(db.String(10000))

# class Ticket_History(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     ticket_number = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.DateTime(timezone=True))
#     device_tag = db.Column(db.Integer, db.ForeignKey('device.asset_tag'))

class Technician(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    records = db.relationship("Record")

# Table for Login Authentication
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))