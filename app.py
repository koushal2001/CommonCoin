from flask import Flask,render_template,flash,redirect,url_for,session,request,logging
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from database import *
from forms import *
app =Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'commonchain'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
mysql.init_app(app)

@app.route("/register" , methods={'GET','POST'})
def register():
    form=Register(request.form)
    users=table("users","Name","Email","username","password")

    if request.method == 'POST' and form.validate():
        pass

    return render_template('register.html')
@app.route("/")
def index():

    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = '123123'
    app.run(debug = True)