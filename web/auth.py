from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from flask_login import login_required, logout_user, current_user, login_user
from .models import User, Employee, Hotel, Payment, Booking
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from . import db
import pdfkit
import sqlite3

'''Using Blueprint as architecture approach and security plugin. Includes the templates and static files that will be 
served on those routes '''

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Erfolgreich eingeloggt!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Falsches Passwort', category='error')
        else:
            flash('E-Mail nicht gefunden.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        passwordconfirm = request.form.get('passwordconfirm')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('E-Mail bereits vorhanden.')
        elif len(email) < 4:
            flash('E-Mail überprüfen.', category='error')
        elif len(password) < 6:
            flash('Bitte ein komplexes Passwort wählen mit mehr als 6 Zeichen.', category='error')
        elif password != passwordconfirm:
            flash('Passwörter sind nicht identisch.', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(passwordconfirm, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Erfolgreich registriert.', category='success')
            return redirect(url_for('auth.login'))

    return render_template("signup.html", user=current_user)


@auth.route('/detail')
@login_required
def detail():
    return render_template("detail.html")


@auth.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    if request.method == 'POST':
        institution = request.form.get('institution')
        cardType = request.form.get('cardType')
        cardholder = request.form.get('cardholder')
        valid = request.form.get('valid')
        cardnumber = request.form.get('cardnumber')

        new_payment = Payment(institution=institution, cardType=cardType, cardholder=cardholder,
                              valid=valid, cardnumber=cardnumber)
        db.session.add(new_payment)
        db.session.commit()
        return redirect(url_for('auth.cc'))

    return render_template("payment.html")


@auth.route('/employee', methods=['GET', 'POST'])
@login_required
def employee():
    if request.method == 'POST':
        empname = request.form['empname']
        fname = request.form['fname']
        tel = request.form['tel']
        emailemp = request.form['emailemp']
        new_employee = Employee(empname=empname, fname=fname, tel=tel, emailemp=emailemp)
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('views.home'))

    return render_template("employee.html")


@auth.route('/hotel', methods=['GET', 'POST'])
@login_required
def hotel():
    if request.method == 'POST':
        hotelname = request.form.get('hotelname')
        street = request.form.get('street')
        zip = request.form.get('zip')
        place = request.form.get('place')
        tel = request.form.get('tel')
        fax = request.form.get('fax')
        email = request.form.get('email')
        new_hotel = Hotel(hotelname=hotelname, street=street, zip=zip, place=place, tel=tel, fax=fax, email=email)
        db.session.add(new_hotel)
        db.session.commit()
        return redirect(url_for('views.home'))
    return render_template("/hotel.html")


@auth.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    if request.method == 'POST':
        ed = request.form.get('ed')
        hn = request.form.get('hn')
        checkinn = request.form.get('checkin')
        checkin = datetime.strptime(checkinn, '%Y-%m-%d')
        checkoutt = request.form.get('checkout')
        checkout = datetime.strptime(checkoutt, '%Y-%m-%d')
        price = request.form.get('price')
        art = request.form.get('art')
        bDate = request.form.get('bookDate')
        bookDate = datetime.strptime(bDate, '%Y-%m-%d')
        new_booking = Booking(ed=ed, hn=hn, checkin=checkin, checkout=checkout, price=price, art=art, bookDate=bookDate)
        db.session.add(new_booking)
        db.session.commit()
        return redirect(url_for('views.home'))
    book = Booking.query.all()
    connect = sqlite3.connect('instance/database.db')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM hotel order by id")
    hotelnamedata = cursor.fetchall()
    print(hotelnamedata)
    cursoremp = connect.cursor()
    cursoremp.execute("SELECT * FROM employee")
    employeedata = cursoremp.fetchall()
    print(employeedata)
    connect.close()
    return render_template("/booking.html", book=book, hotelnamedata=hotelnamedata, employeedata=employeedata)

@auth.route('/preview', methods=['GET','POST'])
@login_required
def preview():
    connect = sqlite3.connect('instance/database.db')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM booking")
    bookingdata = cursor.fetchall()
    connect.close()
    return render_template("/preview.html", bookingdata=bookingdata)


@auth.route('/generatepdf')
@login_required
def pdf_template():
    renderd = render_template('generatepdf.html')
    pdf = pdfkit.from_string(renderd, False)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=buchung.pdf'
    return response


@auth.route('/cc')
@login_required
def cc():
    connect = sqlite3.connect('instance/database.db')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM payment")
    print("DB Data")
    paymentdata = cursor.fetchall()
    print(paymentdata)
    connect.close()
    return render_template("cc.html", paymentdata=paymentdata)

