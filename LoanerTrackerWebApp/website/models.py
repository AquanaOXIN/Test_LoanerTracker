from . import db
from sqlalchemy.sql import func

class Device(db.Model):
    asset_tag = db.Column(db.Integer, primary_key=True)
    device_type = db.Column(db.String(150))
    status = db.Column(db.String(150))
    current_ticket = db.Column(db.Integer)
    tech_id = db.Column(db.Integer, db.ForeignKey('technician.id'))
    out_date = db.Column(db.DateTime(timezone=True))
    note = db.Column(db.String(10000))
    tickets_history = db.relationship('Ticket_History')

class Technician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))

class Ticket_History(db.Model):
    ticket_number = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    