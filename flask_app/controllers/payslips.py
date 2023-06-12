from flask_app import app
from flask import Flask, render_template,session, request, redirect, flash
from flask_app.models.entreprise import Entreprise
from flask_app.models.employee import Employee
from flask_app.models.payslip import Payslip
from flask_app.models.work_time import Work_time
from datetime import datetime


@app.route('/generate_payslip')
def generate():
    employees = Employee.get_all({'entreprise_id':session['entreprise_id']})
    for employee in employees:
        time= Work_time.get_by_id({'employee_id':employee.id})
        if time.work_hours > 208:
            o=time.work_hours-208
            m=0
        else:
            o=0
            m=26-time.work_hours/8
        data = {
            'base_salary':employee.base_salary,
            'employee_id':employee.id,
            'entreprise_id':session['entreprise_id'],
            'overtime':o,
            'missed_days':m,
            'date':datetime.now()
        }
        Payslip.add(data)
    return redirect('/dashboard')

@app.route('/payslip/<payslip_id>')
def show_pay(payslip_id):
    pay=Payslip.get_by_id({'id':payslip_id})
    return render_template("payslip_view.html", payslip=pay)


# @app.route('create/payslip',methods=['POST'])
# def create_payslip():
#     if(Payslip.validate(request.form)):
#       data={** request.form,'entreprise_id':session['entreprise_id']}
#       Payslip.add(data)
#       return redirect('/payslip')
#     return redirect('/dashbord')
# @app.route('/payslips/month', methods=['POST'])
# def payslip_month():
#     print(request.form["month"])
#     monthtolist=[]
#     if request.form["month"]!='':
#         monthtolist=request.form["month"].split("-")
#         session["monthtolist"]=monthtolist
#         session["pmonth"]=Payslip.get_by_month({'month':monthtolist[1],'year':monthtolist[0]})
    
#     return redirect("/dashboard")
