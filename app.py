from flask import Flask,render_template,flash,redirect,url_for,session,request,logging
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from database import *
from forms import *
from functools import wraps

app =Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'commonchain'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            #flash("Unauthorized, please login.", "danger")
            return redirect(url_for('login'))
    return wrap


def log_in(username):
    users=table("users","Name","Email","username","password")
    user=users.getone("username",username)

    session['logged_in']=True
    session['username']=username
    session['name']=user.get('Name')
    session['email'] = user.get('Email')

@app.route("/register" , methods={'GET','POST'})
def register():
    form=Register(request.form)
    users=table("users","Name","Email","username","password")

    if request.method == 'POST':# and form.validate():  //Do this to validate your form
        name=form.name.data
        email=form.email.data
        username=form.username.data
        password=form.password.data
        confirm=form.confirm.data
        if(password == confirm):
            step=True
        if step and isnewuser(username):
            users.insert(name,email,username,password)     # implement SHA_256 hereTrue
            log_in(username)
            return redirect(url_for('dashboard'))
        else:
            pass
            #code to flash messages alert and other errors

    return render_template('register.html')

@app.route("/login" , methods={'GET','POST'})
def login():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']
        users = table("users", "Name", "Email", "username", "password")
        user = users.getone("username", username)
        check=user.get('password')
        if check is None:
            print("here")
            return "user Not found"  #Flash messages to be incoporated
        if check==password:
            log_in(username)
            return redirect(url_for('dashboard'))
        else:
            return "invalid password" #flash message


    return render_template('login.html')

@app.route("/logout")
@is_logged_in
def logout():
    session.clear()
    #flash mesages
    return redirect(url_for('login'))
@app.route("/dashboard")
@is_logged_in
def dashboard():
    return render_template('dashboard.html',session=session)
@app.route("/")
def index():
    check_chain()
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = '123123'
    app.run(debug = True)