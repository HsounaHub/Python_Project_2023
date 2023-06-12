from flask_app import app
from flask import Flask, render_template,session, request, redirect, flash
from flask_app.utilites.utilities import Utilities
from flask_app.models.entreprise import Entreprise
from flask_app.models.employee import Employee
from flask_app.models.payslip import Payslip
from flask_app.models.work_time import Work_time
from flask_bcrypt import Bcrypt

import string,secrets
from datetime import datetime,time
bcrypt = Bcrypt(app)



def password_gen():
    password = ""
    for _ in range(3):
        password += secrets.choice(string.ascii_lowercase)
        password += secrets.choice(string.ascii_uppercase)
        password += secrets.choice(string.digits)
    return(password)

@app.route('/reset_password')
def reset_password():
    # if 'entreprise_id' in session:
    return render_template('reset_password.html')
    # return redirect('/')

@app.route('/users/reset', methods=['POST'])
def emp_reset():
    employee_from_db = Employee.get_by_email({'email':request.form['email']})
    if(employee_from_db):
        password = password_gen()
        Employee.update_password({'password':password,'id':employee_from_db.id})
        Utilities.send_mail("entrepriseproject8@gmail.com",request.form['email'],"Your New Login informations","Your password has been reset. Here is your New one: "+password,"hustmkrguzpdxptv")
        return redirect('/login_entreprise')
    entreprise_from_db = Entreprise.get_by_email({'email':request.form['email']})
    if(entreprise_from_db):
        password = password_gen()
        pw_hash = bcrypt.generate_password_hash(password)

        Entreprise.update_password({'password':pw_hash,'id':entreprise_from_db.id})
        Utilities.send_mail("entrepriseproject8@gmail.com",request.form['email'],"Your New Login informations","Your password has been reset. Here is your New one: "+password,"hustmkrguzpdxptv")
        return redirect('/login_entreprise')
    return redirect('/reset_password')

@app.route('/add_employee')
def add_employee():
    # if 'entreprise_id' in session:
    return render_template('new_employe.html')
    # return redirect('/')

@app.route('/create_employee',methods=['POST'])
def create_employee():
    if(Employee.validate(request.form)):
        # pw_hash = bcrypt.generate_password_hash(request.form['password'])
        # print(pw_hash)
        # data = {
        #     **request.form,'password':pw_hash
        # }
        password=password_gen()
        data = {
            **request.form,'password':password
            ,'status':1
            ,'entreprise_id':session['entreprise_id']
            ,'holidays':0
        }
        # entreprise_id = Employee.add(data)
        # session['entreprise_id'] = entreprise_id
        emp=Employee.add(data)
        Work_time.new({'employee_id':emp})
        Utilities.send_mail("entrepriseproject8@gmail.com",request.form['email'],"Your New Login informations","Your new account has been created. Here is your Password: "+password,"hustmkrguzpdxptv")
        return redirect('/dashboard')
    return redirect('/')

@app.route('/login_employee')
def login_employee():
    # if 'entreprise_id' in session:
    return render_template('employee_login.html')
    # return redirect('/')


@app.route('/employee/login', methods=['POST'])
def emp_login():
    employee_from_db = Employee.get_by_email({'email':request.form['email']})
    if(employee_from_db):
        # if not bcrypt.check_password_hash(employee_from_db.password, request.form['password']):
        if (employee_from_db.password != request.form['password']):
            flash("Invalid Password","log")
            return redirect('/login_employee')
        session['employee_id'] = employee_from_db.id
        session['entreprise_id'] = employee_from_db.entreprise_id
        Work_time.login({'login_time': datetime.now(),'employee_id':session['employee_id']})

        return redirect('/dashboard_employee')
    flash("Invalid Email","log")
    return redirect('/login_employee')

@app.route('/dashboard_employee')
def dash_employee():
    if not 'employee_id' in session:
        return redirect('/')
    employee = Employee.get_by_id({'id':session['employee_id']})
    payslips = Payslip.get_by_employee_id({'employee_id':session['employee_id']})

    return render_template('employee_dashboard.html', employee=employee,payslips=payslips)

@app.route('/logout_employee')
def logout_employee():
    data =Work_time.get_by_id({'employee_id':session['employee_id']})
    logint = data.login_time
    diff = datetime.now()-logint
    sess_s=diff.total_seconds()
    sess_h=sess_s/(60*60)
    print(sess_h)
    Work_time.logout({'logout_time': datetime.now(),'employee_id':session['employee_id'],'work_hours':data.work_hours+sess_h})
    session.clear()
    return redirect('/')