from flask import Blueprint, render_template, request, session, redirect
import re
from ..models.my_data import Users
from ..models.my_data import db
from flask_session import Session

from .. import app

auth = Blueprint('auth', __name__)
UPLOAD_FOLDER = 'user_data/uploads_emotion_detection'
# app.config['UPLOAD_FOLDER'] = "D:/programming/ITI/Flask/alproject/app/user_data/videos"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Login Function
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    else:
        email = request.form['email']
        password = request.form['password1']
        check_user = Users.query.filter_by(email=email, password=password).first()

        # If user is found
        if check_user is not None:
            fullname = check_user.fullname
            email = check_user.email

            # Adding to the Session
            session['fullname'] = fullname
            session['email'] = email

            # Going to Homepage
            return render_template('home/home.html', fullname=fullname, score=None, solid_line=None)
        else:
            login_problem = 'email and/or password are not correct'
            return render_template('auth/login.html', login_problem=login_problem)


# REGISTER FUNCTION
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        print("GET METHOD ")
        return render_template('auth/register.html')

    else:
        fullname = request.form['fullname']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        phone = request.form['phone']

        comm_email, comm_sms, comm_phone = False, False, False
        if request.form.get("comm_phone"):
            comm_phone = True
        if request.form.get("comm_email"):
            comm_email = True
        if request.form.get("comm_sms"):
            comm_sms = True

        # Checking if Email is already Registered
        email_request = Users.query.filter_by(email=email).first()
        if email_request:
            email_exists = "This Email is Already registered.."
            return render_template('auth/register.html', email_exists=email_exists)

        # Checking Password Match
        elif password1 != password2:
            password_not_match = "The passwords are not identical.."
            return render_template('auth/register.html', password_not_match=password_not_match)

        # If No Problem --> Register the user
        else:
            new_user = Users(fullname=fullname, password=password1, email=email, phone=phone,
                               comm_email=comm_email, comm_sms=comm_sms, comm_phone=comm_phone)
            db.session.add(new_user)
            db.session.commit()
            return render_template('auth/login.html', fullname=fullname)


# LOGOUT
@auth.route('/logout')
def logout():
    session.clear()
    return render_template('auth/login.html')
