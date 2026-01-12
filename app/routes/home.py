from flask import render_template
from flask_login import current_user

def home():
    if current_user.is_authenticated:
        return render_template("home.html")
    return render_template("home_unauth.html")