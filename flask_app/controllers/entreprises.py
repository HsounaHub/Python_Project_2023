from flask_app import app
from flask import Flask, render_template,session, request, redirect, flash
from flask_app.models.entreprise import Entreprise
from flask_app.models.employee import Employee
from flask_app.models.payslip import Payslip
from flask_app.models.work_time import Work_time
from flask_bcrypt import Bcrypt
import datetime
from flask_app.utilites.utilities import Utilities
bcrypt = Bcrypt(app)

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if not 'entreprise_id' in session:
        return redirect('/')
    # payslips = Payslip.get_all({'entreprise_id':session['entreprise_id']})
    # employees = Employee.get_all({'entreprise_id':session['entreprise_id']})
    # entreprise = Entreprise.get_by_id({'id':session['entreprise_id']})
    monthtolist=[]
    if len(monthtolist)<1:
        date = datetime.date.today()
        monthtolist=date.strftime('%Y-%m').split("-")
        year_month=date.strftime('%Y-%m')
    if request.method == 'POST':
        if request.form["month"]!='':
            monthtolist=request.form["month"].split("-")
            year_month=request.form["month"]
        else:
            monthtolist=["",""]
            year_month=""
    print(monthtolist)
    # Pmonth=Payslip.get_by_month({'month':monthtolist[1],'year':monthtolist[0],'entreprise_id':session['entreprise_id']})
    print(year_month)
    allempol=Employee.get_all_employees_payslips()
    print(allempol[0].payslip.date)
    return render_template("dashboard.html",allempol=allempol,monthtolist=monthtolist,month_6=Utilities.get_last_6_months(),year_month=year_month,name_empol_list=[])

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
    
    employee_from_db = Employee.get_by_email({'email':request.form['email']})
    if(employee_from_db):
        # if not bcrypt.check_password_hash(employee_from_db.password, request.form['password']):
        if (employee_from_db.password != request.form['password']):
            flash("Invalid Password","log")
            return redirect('/login_employee')
        session['employee_id'] = employee_from_db.id
        session['entreprise_id'] = employee_from_db.entreprise_id
        Work_time.login({'login_time': datetime.datetime.now(),'employee_id':session['employee_id']})
        return redirect('/dashboard_employee')

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