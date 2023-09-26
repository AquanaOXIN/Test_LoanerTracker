# Stores standard routes for the website (excl. login)

from flask import Blueprint, render_template, request, flash

views = Blueprint('views', __name__) # a blueprint for the flask web app

@views.route('/') 
def home():
    test_mode = True
    return render_template("home.html", boolean=test_mode)

@views.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        data = request.form.get('assetTag') # Pull information based on the "name" attribute
        print(data)
    return render_template("test.html")
