from flask_app import app
from flask import Flask, render_template,session, request, redirect, flash
from flask_app.models.entreprise import Entreprise
from flask_app.models.employee import Employee
from flask_app.models.payslip import Payslip
from flask_bcrypt import Bcrypt
import datetime
from flask_app.utilites.utilities import Utilities
bcrypt = Bcrypt(app)

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if not 'entreprise_id' in session:
        return redirect('/')
    # payslips = Payslip.get_all({'entreprise_id':session['entreprise_id']})
    employees = Employee.get_all({'entreprise_id':session['entreprise_id']})
    entreprise = Entreprise.get_by_id({'id':session['entreprise_id']})
    monthtolist=[]
    if len(monthtolist)<1:
        date = datetime.date.today()
        monthtolist=date.strftime('%Y-%m').split("-")
    if request.method == 'POST':
        print("-"*20+request.form["month"])
        if request.form["month"]!='':
            monthtolist=request.form["month"].split("-")
        else:
            monthtolist=["",""]
    Pmonth=Payslip.get_by_month({'month':monthtolist[1],'year':monthtolist[0]})
    print(Utilities.get_last_6_months())
    return render_template("dashboard.html", entreprise = entreprise , employees=employees,pmonth=Pmonth,monthtolist=monthtolist,month_6=Utilities.get_last_6_months())

@app.route('/add_entreprise')
def add_entreprise():
    # if 'entreprise_id' in session:
    return render_template('sign_up_page.html')
    # return redirect('/')

@app.route('/login_entreprise')
def login_entreprise():
    # if 'entreprise_id' in session:
    return render_template('login_page.html')
    # return redirect('/')

@app.route('/users/login', methods=['POST'])
def login():
    entreprise_from_db = Entreprise.get_by_email({'email':request.form['email']})
    if(entreprise_from_db):
        if not bcrypt.check_password_hash(entreprise_from_db.password, request.form['password']):
            flash("Invalid Password","log")
            return redirect('/login_entreprise')
        session['entreprise_id'] = entreprise_from_db.id
        return redirect('/dashboard')
    flash("Invalid Email","log")
    return redirect('/login_entreprise')

@app.route('/entreprise/create',methods=['POST'])
def create_entreprise():
    if(Entreprise.validate(request.form)):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            **request.form,'password':pw_hash
        }
        entreprise_id = Entreprise.create(data)
        session['entreprise_id'] = entreprise_id
        return redirect('/dashboard')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/')
def index():
    if 'entreprise_id' in session:
        return redirect("/dashboard")
    return render_template("index.html")