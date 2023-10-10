from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__) 

### TO BE REMOVED
secret_hash = 'scrypt:32768:8:1$7VEj7HvoMjetWwEH$21537867c0f5c2670a6ea7738dfc17f23f70e9ecb8951b4180eeee0f7be7c7c1c6b894e877978ec16f90b47a225cb1c7f576defbad9daf9cfeae93337de8e8d6'

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        ### TO BE CHANGED
        secret_code = request.form.get('secretCode')
        if check_password_hash(secret_hash, secret_code):
            ### TO BE CHANGED
            user = User.query.filter_by(id=0).first()
            flash('Logged in successfully!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('Invalid Code, iNtRuDeR!!!', category='error')
    
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
