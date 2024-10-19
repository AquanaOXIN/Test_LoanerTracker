from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from . import views
from .config import SECRET_HASH  # modified here ...

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if "colorModeIcon" in request.form:
            views.color_toggle()
        else:
            secret_code = request.form.get('secretCode')
            if check_password_hash(SECRET_HASH, secret_code):  # modified here ...
                user = User.query.filter_by(id=0).first()
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Invalid Code, iNtRuDeR!!!', category='error')

    return render_template("login.html", user=current_user, dark_mode=views.dark_mode)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))