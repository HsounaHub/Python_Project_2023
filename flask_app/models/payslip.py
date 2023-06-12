from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import employee

class Payslip :
    def __init__(self,data):
        self.id = data['id']
        self.missed_days = data['missed_days']
        self.overtime = data['overtime']
        self.date = data['date']
        self.base_salary = data['base_salary']
        self.employee_id = data['employee_id']
        self.entreprise_id = data['entreprise_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.brut = self.brut_calc()
        self.cnss = self.brut*0.0918
        self.imposable=self.brut-self.cnss
        self.retenue = self.retenue_calc()
        self.sociale= self.retenue*0.04
        self.net= self.imposable-self.retenue-self.sociale
        self.employee=employee.Employee.get_by_id({"id":self.employee_id})

    @classmethod
    def get_all(cls,data):
        query = """
        SELECT * FROM payslips WHERE entreprise_id = %(entreprise_id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        emps = []
        for row in results:
            emps.append(cls(row))
        return emps
    

    
    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * FROM payslips WHERE id = %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])



    @classmethod
    def add(cls, data):
        query = """
        INSERT INTO payslips (missed_days,overtime,date,base_salary,employee_id,entreprise_id) 
        VALUES (%(missed_days)s,%(overtime)s,%(date)s,%(base_salary)s,%(employee_id)s,%(entreprise_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_by_employee_id(cls, data):
        query = """
        SELECT * FROM payslips WHERE employee_id = %(employee_id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        if result:
            emps = []
            for row in result:
                emps.append(cls(row))
            return emps
        else:
            return [0]

    @classmethod
    def delete(cls, data):
        query = """
        delete from payslips where id=%(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def edit(cls, data):
        query = """
        UPDATE payslips SET missed_days=%(missed_days)s,overtime=%(overtime)s,date=%(date)s,base_salary=%(base_salary)s,employee_id=%(employee_id)s,entreprise_id=%(entreprise_id)s,worktime_id%(worktime_id)s
        WHERE id = %(id)s;
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

    def brut_calc(self):
        h_salary=self.base_salary/208
        hours=208
        hours=hours-self.missed_days*8
        hours=hours+self.overtime
        if hours<=208:
            return h_salary*hours
        else:
            return (h_salary*208)+(((hours-208)*1.5)*h_salary)

    def retenue_calc(self):
        anual_impo=self.imposable*12
        if anual_impo <= 5000:
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
    def get_by_month(cls, data):
        query = """
        select *from payslips where month(date)=%(month)s and year(date)=%(year)s and entreprise_id = %(entreprise_id)s ;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        if result:
            slips = []
            for row in result:
                slips.append(cls(row))
            return slips
        else:
            return [0]
    