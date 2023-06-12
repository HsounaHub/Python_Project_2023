from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import payslip

class Employee :
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.cin = data['cin']
        self.phone=data['phone']
        self.email=data['email']
        self.password = data['password']
        self.function = data['efunction']
        self.status=data['status']
        self.entreprise_id = data['entreprise_id']
        self.cnss=data['cnss']
        self.base_salary=data['base_salary']
        self.holidays=data['holidays']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.payslip = payslip.Payslip.get_by_employee_id({'employee_id':self.id})

    @classmethod
    def get_all(cls,data):
        query = """
        SELECT * FROM employees WHERE entreprise_id = %(entreprise_id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        emps = []
        for row in results:
            emps.append(cls(row))
        return emps

    @classmethod
    def add(cls, data):
        query = """
        INSERT INTO employees ( first_name, last_name,cin,phone,email,password,efunction,status,entreprise_id,cnss,holidays,base_salary) 
        VALUES (%(first_name)s,%(last_name)s,%(cin)s,%(phone)s,%(email)s,%(password)s,%(function)s,%(status)s,%(entreprise_id)s,%(cnss)s,%(holidays)s,%(base_salary)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['first_name'])< 2:
            flash("first_name must be at least 3")
            is_valid = False
        if len(data['last_name'])< 2:
            flash("last_name too short")
            is_valid = False
        if len(data['cin']) != 8:
            flash("CIN must be 8 numbers")
            is_valid = False
        if len(data['function']) < 2:
            flash("function error")
            is_valid = False
        if int(data['base_salary'])  < 400:
            flash("minimum base salarys is 400")
            is_valid = False
        return is_valid
    
    # @classmethod
    # def delete(cls, data):
    #     query = """
    #     delete from employees where id=%(id)s;
    #     """
    #     return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def edit(cls, data):
        query = """
        UPDATE employees
        SET first_name = %(first_name)s, last_name = %(last_name)s, cin= %(cin)s ,phone=%(phone)s,email=%(email)s,password=%(password)s,function = %(function)s,status= %(status)s,entreprise_id=%(entreprise_id)s,cnss=%(cnss)s,holidays=%(holidays)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * FROM employees WHERE id = %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])
    

    @classmethod
    def get_by_email(cls,data):
        query = """
        SELECT * FROM employees WHERE email = %(email)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        if(result):
            return cls(result[0])
        return False
    