from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session  # modified here ...
from flask_login import login_required, current_user
from datetime import datetime, date, time, timezone
from .models import Device, Record
from . import db
import re
import json
import pandas as pd

test_mode = True

views = Blueprint('views', __name__) 

IS_AVAILABLE = "Available"
IS_INUSE = "In-Use"
IS_RETIRED = "Retired"
IS_UNKNOWN = "Unknown"

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if "colorModeIcon" in request.form:
            color_mode = color_toggle()

    # modified here ...
    dark_mode = session.get('dark_mode', True)  
    return render_template("home.html", test_mode=test_mode, user=current_user, dark_mode=dark_mode)

@views.route('/records', methods=['GET', 'POST'])
@login_required
def records():
    if request.method == 'POST':
        if "colorModeIcon" in request.form:
            color_mode = color_toggle()
    records = Record.query.all()

    # modified here ...
    dark_mode = session.get('dark_mode', True)
    return render_template("records.html", records=records, test_mode=test_mode, user=current_user, dark_mode=dark_mode)

@views.route('/devices', methods=['GET', 'POST'])
@login_required
def devices():
    if request.method == 'POST':
        if "colorModeIcon" in request.form:
            color_mode = color_toggle()
    devices = Device.query.all()

    # modified here ...
    dark_mode = session.get('dark_mode', True)  
    return render_template("devices.html", devices=devices, test_mode=test_mode, user=current_user, dark_mode=dark_mode)

@views.route('/loan-out', methods=['GET', 'POST'])
@login_required
def loan_out():
    if request.method == 'POST':
        if "colorModeIcon" in request.form:
            color_mode = color_toggle()
        else:
            asset_tag = request.form.get('assetTag')
            ticket_number = request.form.get('ticketNumber')
            tech_name = request.form.get('techName')
            time_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            current_time = pd.to_datetime(time_string).to_pydatetime()
            note = request.form.get('note')

            device = Device.query.filter_by(asset_tag=asset_tag).first()
            if device:
                if device.device_status != IS_AVAILABLE:
                    flash('Loaner '+ asset_tag +' is NOT AVAILABLE!', category='error')
                else:
                    new_record = Record(asset_tag=asset_tag, ticket_number=ticket_number, tech_name=tech_name, out_date=current_time, note=note)
                    device.device_status = IS_INUSE
                    db.session.add(new_record)
                    db.session.commit()
                    flash('Loaner '+ asset_tag +' has been successfully loaned out!', category='success')
            else:
                flash('Loaner '+ asset_tag +' is NOT in the loaner database!', category='error')
                flash('If the device is a loaner, please add it into the database through \'New Device\' first.', category='warning')

            return redirect(url_for('views.loan_out'))

    # modified here ...
    dark_mode = session.get('dark_mode', True)  
    return render_template("loan-out.html", test_mode=test_mode, user=current_user, dark_mode=dark_mode)

@views.route('/turn-in', methods=['GET', 'POST'])
@login_required
def turn_in():
    if request.method == 'POST':
        if "colorModeIcon" in request.form:
            color_mode = color_toggle()
        else:
            asset_tag = request.form.get('assetTag')
            ticket_number = request.form.get('ticketNumber')
            tech_name = request.form.get('techName')
            time_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            current_time = pd.to_datetime(time_string).to_pydatetime()
            return_note = request.form.get('note')

            record = Record.query.filter_by(asset_tag=asset_tag, ticket_number=ticket_number).first()
            if record:
                device = Device.query.filter_by(asset_tag=asset_tag).first()
                if device.device_status == IS_INUSE:
                    record.in_date = current_time
                    device.device_status = IS_AVAILABLE
                    record.note += " || Return note: " + return_note
                    if tech_name != record.tech_name:
                        record.note += " || Returned by: " + tech_name
                    db.session.commit()
                    flash('Loaner '+ asset_tag +' has been successfully returned!', category='success')
                elif device.device_status == IS_AVAILABLE:
                    flash('Loaner '+ asset_tag +' is not loaned out!', category='error')
                elif device.device_status == IS_RETIRED:
                    flash('Loaner '+ asset_tag +' is already marked as RETIRED!', category='error')
                elif device.device_status == IS_UNKNOWN:
                    flash('Loaner '+ asset_tag +' status missing, please see admin!', category='error')
                else:
                    flash('Something went wrong!', category='error')
            else:
                flash('Cannot locate the loan-out record for the device corresponding to the ticket!', category='error')

            return redirect(url_for('views.turn_in'))
        
    # modified here ...
    dark_mode = session.get('dark_mode', True)  
    return render_template("turn-in.html", test_mode=test_mode, user=current_user, dark_mode=dark_mode)

@views.route('/add-device', methods=['GET','POST'])
@login_required
def add_device():
    if request.method == 'POST':
        if "colorModeIcon" in request.form:
            color_mode = color_toggle()
        else:
            asset_tag = request.form.get('assetTag')
            device_type = request.form.get('deviceType')
            device_status = request.form.get('deviceStatus')
            note = request.form.get('note')

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

    # modified here ...
    dark_mode = session.get('dark_mode', True)
    return render_template("add-device.html", test_mode=test_mode, user=current_user, dark_mode=dark_mode)

@views.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    if request.method == 'POST':
        if "colorModeIcon" in request.form:
            color_mode = color_toggle()
        else:
            data = request.form.get('assetTag') 
            print(data)
    
    # modified here ...
    dark_mode = session.get('dark_mode', True)  
    return render_template("test.html", test_mode=test_mode, user=current_user, dark_mode=dark_mode)

def color_toggle():
    current_color_mode = request.form.get('colorModeIcon')
    if current_color_mode == "isDark":
        # modified here ...
        session['dark_mode'] = False
    else:
        # modified here ...
        session['dark_mode'] = True
    return session['dark_mode']

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