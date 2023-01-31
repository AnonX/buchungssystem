from flask import Blueprint, render_template
from flask_login import login_required, current_user
import sqlite3


views = Blueprint('views', __name__)


# Decorator view for blueprint
@views.route('/home')
@login_required
def home():
    connect = sqlite3.connect('instance/database.db')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM booking")
    print("DB Data")
    bookingdata = cursor.fetchall()
    print(bookingdata)
    return render_template("home.html",user=current_user, bookingdata=bookingdata)