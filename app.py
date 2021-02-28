from flask import Flask,render_template,flash,redirect,url_for,session,request,logging
from passlib.hash import sha256_crypt
from flaskext.mysql import MySQL

app =Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD'] = 'Tacmp@1234'
app.config['MYSQL_DB'] = 'commonchain'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = '123123'
    app.run(debug = True)