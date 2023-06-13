from flask_app import app
from flask import Flask, render_template,session, request, redirect, flash
from flask_app.models.entreprise import Entreprise
from flask_app.models.employee import Employee
from flask_app.models.ticket import Tickets
from flask_bcrypt import Bcrypt
from datetime import datetime,time
bcrypt = Bcrypt(app)

# @app.route('/employee/dashboard')
# def add():
#   if 'employee_id' in session:
#       if 'entreprise_id' in session:
#           return render_template('ticket.html')
#   return redirect('/')

@app.route('/create_ticketsss',methods=['POST'])
def create_ticket():
    print(request.form)
    empol=Employee.get_by_id({'id':session['employee_id']})
    data={**request.form,'employee_id':session['employee_id'],'entreprise_id':empol.entreprise_id}
    Tickets.add_ticket(data)
    return redirect('dashboard_employee')

@app.route('/ticket/view/<int:id>')
def show_view(id):
  if 'entreprise_id' in session:
      data={'id':id}
      tick=Tickets.get_by_id(data)
      # entre=Entreprise.get_by_id_enterprise_id({"id":session['entreprise_id']})
      emp=Employee.get_by_id({'id':tick.employee_id})
      
      return render_template("view.html",tick=tick,emp=emp)
  return redirect('/')

@app.route('/employee/ticket/edit/<int:id>')
def show_edit(id):
    if "entreprise_id" in session:
        data={'id':id}
        e=Tickets.get_by_id(data)
        return render_template("edit_ticket.html",tick=e)
    return redirect('/')

@app.route('/employee/ticket/update/<int:id>',methods=['POST'])
def update(id):
    if "entreprise_id" in session:
       data={
        **request.form,
        'id':id,
        'closed_date':datetime.now()
        }
       Tickets.edit_ticket(data)
       return redirect('/dashboard_employee')
    return redirect('/')
