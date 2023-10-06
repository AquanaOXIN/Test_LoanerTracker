# Stores standard routes for the website (excl. login)

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime, date, time, timezone
from .models import Device, Record
from . import db
import re
import json
import pandas as pd

### TEST MODE TOGGLE
test_mode = True

views = Blueprint('views', __name__) # a blueprint for the flask web app

IS_AVAILABLE = "Available"
IS_INUSE = "In-Use"
IS_RETIRED = "Retired"
IS_UNKNOWN = "Unknown"

@views.route('/') 
@login_required
def home():
    
    return render_template("home.html", boolean=test_mode, user=current_user)

@views.route('/records')
@login_required
def records():
    records = Record.query.all()
    return render_template("records.html", records=records, boolean=test_mode, user=current_user)

@views.route('/loan-out', methods=['GET', 'POST'])
@login_required
def loan_out():
    if request.method == 'POST':
        asset_tag = request.form.get('assetTag')
        ticket_number = request.form.get('ticketNumber')
        tech_name = request.form.get('techName')
        # current_time = datetime.now(tz=None)
        time_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        current_time = pd.to_datetime(time_string).to_pydatetime()
        note = request.form.get('note')

        device = Device.query.filter_by(asset_tag=asset_tag).first()
        if device:
            ### CHECK IF DEVICE IS NOT AVAILABLE
            if device.device_status != IS_AVAILABLE:
                flash('Loaner '+ asset_tag +' is NOT AVAILABLE!', category='error')
            else:
                new_record = Record(asset_tag=asset_tag, ticket_number=ticket_number, tech_name=tech_name, out_date=current_time, note=note)
                device.device_status = IS_INUSE
                db.session.add(new_record)
                db.session.commit()
                flash('Loaner '+ asset_tag +' has been successfully loaned out!', category='success')
        else:
            # new_record = Device(asset_tag=asset_tag, tech_name=tech_name, current_ticket=current_ticket, out_date=current_time)
            # db.session.add(new_record)
            # db.session.commit()
            flash('Loaner '+ asset_tag +' is NOT in the loaner database!', category='error')
            flash('If the device is a loaner, please add it into the database through \'New Device\' first.', category='warning')
        
        return redirect(url_for('views.loan_out'))
    
    return render_template("loan-out.html", boolean=test_mode, user=current_user)
        

@views.route('/add-device', methods=['GET','POST'])
@login_required
def add_device():
    if request.method == 'POST':
        asset_tag = request.form.get('assetTag')
        device_type = request.form.get('deviceType')
        device_status = request.form.get('deviceStatus')
        note = request.form.get('note')
        # device = Device.query.filter_by(asset_tag=asset_tag).first()

        if asset_validation(asset_tag) == False:
            flash('Device Already in Database', category='error')
        elif asset_tag_validation(asset_tag) == False:
            flash('Invalid Asset Tag #', category='error')        
        elif device_type_validation(device_type) == False:
            flash('Unsupported Device Type', category='error')
        elif device_status_validation(device_status) == False:
            flash('How dare you add UNAVAILABLE devices to database!?', category='error')
        else:
            new_device = Device(asset_tag=asset_tag, device_type=device_type, device_status=device_status, note=note)
            db.session.add(new_device)
            db.session.commit()
            flash('Device #' + asset_tag + ' has been successfully added into the database!', category='success')
        
    return render_template("add-device.html", boolean=test_mode, user=current_user)

@views.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    if request.method == 'POST':
        data = request.form.get('assetTag') # Pull information based on the "name" attribute
        print(data)
    return render_template("test.html", user=current_user)

def asset_validation(input_assetTag):
    is_valid = True
    record = Device.query.filter_by(asset_tag=input_assetTag).first()
    if record:
        is_valid = False
    return is_valid

def asset_tag_validation(input_assetTag):
    is_valid = bool(re.match(r'^\d{8}$', input_assetTag))
    return is_valid

def device_type_validation(input_deviceType):
    supported_types = ["laptop STAFF", "laptop STUDENT"]
    is_valid = input_deviceType in supported_types
    return is_valid

def device_status_validation(input_deviceStatus):
    is_valid = input_deviceStatus == "Available"
    return is_valid