from flask import Blueprint, render_template, request, flash


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    print(data)
    return render_template("login.html", text="Testing")

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route('/sign-up')
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        passwordconfirm = request.form.get('passwordconfirm')

        if len(email) < 4:
            flash('E-Mail überprüfen', category='error')
        elif len(password) < 6:
            pass
        elif password != passwordconfirm:
            pass
        elif len(password) < 7:
            pass
        else:
            flash('Erfolgreich angelegt', category='success')

    return render_template("signup.html", methods=['GET', 'POST'])

@auth.route('/home')
def home():
    return"<p>home</p>"
