from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Payslip :
    def __init__(self,data):
        self.id = data['id']
        self.employee_id = data['employee_id']
        self.base_salary = data['base_salary']
        self.holidays = data['holidays']
        self.overtime = data['overtime']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.cnss = self.brut*0.2575
        self.imposable=self.brut-self.cnss
        self.sociale= self.retenue*0.04
        self.net= self.imposable-self.retenue-self.sociale

    def brut(self):
        h_salary=self.base_salary/208
        hours=208
        hours=hours-self.holidays*8
        hours=hours+self.overtime
        if hours<=208:
            return h_salary*hours
        else:
            return (h_salary*208)+(((hours-208)*1.5)*h_salary)

    def retenue(self):
        anual_impo=self.imposable*12
        if anual_impo <= 5000:
            if anual_impo*0.1<2000:
                return 0
        elif anual_impo <= 20000:
            rest =anual_impo*0.9
            return (rest-5000)*0.26/12
        elif anual_impo <= 30000:
            rest =anual_impo*0.9
            return (rest-5000)*0.28/12
        elif anual_impo <= 50000:
            rest =anual_impo*0.9
            return (rest-5000)*0.32/12
        else:
            rest =anual_impo*0.9
            return (rest-5000)*0.35/12

    @classmethod
    def get_all(cls,data):
        query = """
        SELECT * FROM payslips WHERE employee_id = %(employee_id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        emps = []
        for row in results:
            emps.append(cls(row))
        return emps

    @classmethod
    def add(cls, data):
        query = """
        INSERT INTO payslips (employee_id, base_salary, holidays,overtime,date) 
        VALUES (%(employee_id)s,%(base_salary)s,%(holidays)s,%(overtime)s,%(date)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['date']) == "":
            flash("date error")
            is_valid = False
        if data['base_salary'] < 400:
            flash("minimum base salary is 400")
            is_valid = False
        return is_valid