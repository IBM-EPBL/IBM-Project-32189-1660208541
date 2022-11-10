from flask import Flask, render_template, request, redirect, session ,url_for
import ibm_db
import re

app = Flask(__name__)

hostname="125f9f61-9715-46f9-9399-c8177b21803b.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud"
uid="rbc20807"
pwd="oNyTBodONFXlomZY"
driver="{IBM DB2 ODBC DRIVER}"
db="bludb"
port="30426"
protocol="TCP IP"
cert="Certificate.crt"

dsn=(
    "DATABASE={0};"
    "HOSTNAME={1};"
    "PORT={2};"
    "UID={3};"
    "SECURITY=SSL;"
    "SSLServerCertificate={4};"
    "PWD={5};"
).format(db_name, hostname, port, uid, protocol, cert, pwd)
connection = ibm_db.connect(dsn, "", "") 
app.secret_key = 'a'
  

@app.route("/")
def add():
    return render_template("Home.html")

#CHANGE FORGOT PASSWORD

@app.route("/forgot")
def forgot():
    return render_template('forgot.html')
        
@app.route("/forgotpw", methods =['GET', 'POST'])
def forgotpw():
    msg = ''
    if request.method == 'POST' :
        email = request.form['email']
        password = request.form['password']
        query = "SELECT * FROM register WHERE email=?;"
        stmt = ibm_db.prepare(connection, query)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            query = "UPDATE register SET password = ? WHERE email = ?;"
            stmt = ibm_db.prepare(connection, query)
            ibm_db.bind_param(stmt, 1, password)
            ibm_db.bind_param(stmt, 2, email)
            ibm_db.execute(stmt)
            msg = 'Successfully changed your password ! Proceed Login Process'
            return render_template('login.html', msg = msg)
    else:
        msg = 'PLEASE FILL OUT THE CORRECT DETAILS'
        return render_template('forgot.html', msg=msg)


#LOGIN--PAGE
    
@app.route("/signin")
def signin():
    return render_template('login.html')
        
@app.route('/login',methods =['GET', 'POST'])
def login():
    global userid
    msg = ''
  
    if request.method == 'POST' :
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM register WHERE username =? AND password=?;"
        stmt = ibm_db.prepare(connection, sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print (account)
        
        if account:
            session['loggedin'] = True
            session['id'] = account['USERNAME']
            userid=  account['USERNAME']
            session['USERNAME'] = account['USERNAME']
           
            return redirect('/home')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
if __name__ == "__main__":
    app.run(debug=True)