from flask import Flask, render_template,request,redirect,url_for,session,flash
import ibm_db
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import requests

app=Flask(__name__)
app.secret_key='a'


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=19af6446-6171-4641-8aba-9dcff8e1b6ff.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=30699;SECURITY=SSL;SSLServerCertificat=DigiCertGlobalRootCA.crt;UID=mjc12838;PWD=R0w7xxbuh4C1PKHz",'','')
    
@app.route("/")
def dash():
    return render_template('login.html',msg=" ")

@app.route("/register")
def signup():
    return render_template('register.html')

    
@app.route("/register",methods=['GET','POST'])
def register():
    error = None 
    if request.method=='POST':
           username=request.form['username']
           email=request.form['email']
           phone_number=request.form['phonenumber']
           password=request.form['password']
           pin=request.form['pin']
           sql="SELECT * FROM user WHERE username=?"
           prep_stmt=ibm_db.prepare(conn,sql)
           ibm_db.bind_param(prep_stmt,1,username)
           ibm_db.execute(prep_stmt)
           account=ibm_db.fetch_assoc(prep_stmt)
           print(account)
             #message = Mail(from_email='btechmano@gmail.com',to_emails=session['email'],subject="Devnews - Registration",html_content='<b>Devnews welcomes you</b><br/><p>Your account has been registered successfully</p>')
            #try:
                #sg=SendGridAPIClient()
                # Secret key can't be submitted otherwise my 
                # sendgrid accound reporting that i am exposing 
                # my secret key as public and my account will terminated soon
                #response=sg.send(message)
                #print(response.status_code)
                #print(response.body)
                #print(response.headers)
            #except Exception as e:
                #print(e)
           if account:
               error="Account already exists! Log in to continue !"
           else:
               insert_sql="INSERT INTO user values(?,?,?,?,?)"
               prep_stmt=ibm_db.prepare(conn,insert_sql)
               ibm_db.bind_param(prep_stmt,1,email)
               ibm_db.bind_param(prep_stmt,2,username)
               ibm_db.bind_param(prep_stmt,3,phone_number)
               ibm_db.bind_param(prep_stmt,4,password)
               ibm_db.bind_param(prep_stmt,5,pin)
               ibm_db.execute(prep_stmt)
               flash(" Registration successfull. Log in to continue !")
    else:
        pass
    return render_template('welcome.html',error=error)
@app.route("/login")
def signin():
    return render_template('login.html')

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        sql="SELECT * FROM user WHERE username=? AND password=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin']=True
            session['id']=account['USERNAME']
            session["username"]=account["USERNAME"]
            flash("Logged in successfully!")
            return render_template('welcome.html',error=error)
        else:
            error="Incorrect username / password"
            return render_template('login.html')
    

@app.route('/forget',methods=['GET','POST'])
def forget():
    error = None
    if request.method=='POST':
        username=request.form['username']
        pin=request.form['pin']
        sql="SELECT * FROM user WHERE username=? AND pin=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,pin)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin']=True
            session['id']=account['USERNAME']
            session["username"]=account["USERNAME"]
            flash("Logged in successfully!")
            return redirect(url_for("home"))
        else:
            error="Incorrect username / pin"
            return render_template('login.html',error=error)
    return render_template('forget.html',error=error)
    
@app.route('/welcome')
def welcome_page():
    return render_template("welcome.html",msg=" ")
@app.route('/home')
def home():
    return render_template("welcome.html",msg=" ")
@app.route('/skills')
def skills():
    return render_template("skills.html",msg=" ")
@app.route('/about')
def about():
    return render_template("about.html",msg=" ")
@app.route('/contact')
def contact():
    return render_template("contact.html",msg=" ")
if __name__=='__main__':
    
    app.run(debug=True)
