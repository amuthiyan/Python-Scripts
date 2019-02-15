from flask import render_template, flash, redirect, session, g
from app import app
from app import db, models
from .forms import LoginForm, Register

@app.route('/hello')
def index():
    return "Hello, World"

@app.route('/user')
def home():
    user = session['userid']
    return render_template("home.html",
                           title = 'User Page',
                           user = user)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    user = form.userid.data
    password = form.password.data
    if form.validate_on_submit():
        query = models.User.query.filter_by(username = user).first()
        if query is not None:
            if(query.username == user) & (query.password == password):
                flash('Login requested for OpenID="%s", password= "%s"' %
                  (form.userid.data, form.password.data))
                session['userid'] = user
                return redirect('/user')
        else:
            flash('Username/Password is incorrect. Make sure you have registered')
    return render_template("login.html",
                           title = 'Login',
                           form = form)

@app.route('/register',methods=['GET','POST'])
def signin():
    form = Register()
    if form.validate_on_submit():
        username = form.userid.data
        password = form.password.data
        query = models.User.query.filter_by(username = username).first()
        if query is None:
            new_user = models.User(username = username, password = password)
            db.session.add(new_user)
            db.session.commit()
            flash('Thank you for registering')
            return redirect('/login')
        else:
            flash('That username is taken')
    return render_template("register.html",
                           title='Sign_In',
                           form=form)

           
