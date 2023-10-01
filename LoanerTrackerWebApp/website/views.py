# Stores standard routes for the website (excl. login)

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Device
from . import db
import re
import json

views = Blueprint('views', __name__) # a blueprint for the flask web app

@views.route('/') 
@login_required
def home():
    test_mode = True
    return render_template("home.html", boolean=test_mode, user=current_user)

@views.route('/add-device', methods=['GET','POST'])
@login_required
def add_device():
    if request.method == 'POST':
        asset_tag = request.form.get('assetTag')
        device_type = request.form.get('deviceType')
        device_status = request.form.get('deviceStatus')

        # device = Device.query.filter_by(asset_tag=asset_tag).first()

        if asset_tag_validation(asset_tag) == False:
            flash('Invalid Asset Tag #', category='error')
        if device_type_validation(device_type) == False:
            flash('Unsupported Device Type', category='error')
        if device_status_validation(device_status) == False:
            flash('How dare you add UNAVAILABLE devices to database!?', category='error')
        
    return render_template("add-device.html", user=current_user)

@views.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    if request.method == 'POST':
        data = request.form.get('assetTag') # Pull information based on the "name" attribute
        print(data)
    return render_template("test.html", user=current_user)


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