from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import entreprise

class Employee :
    def __init__(self,data):
        self.id = data['id']
        self.entreprise_id = data['entreprise_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.cin = data['cin']
        self.function = data['function']
        self.base_salary = data['base_salary']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.entreprise_name = entreprise.Entreprise.get_by_id({'id':self.entreprise_id}).name

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
        INSERT INTO employees (entreprise_id, first_name, last_name,cin,function,base_salary) 
        VALUES (%(entreprise_id)s,%(first_name)s,%(last_name)s,%(cin)s,%(function)s,%(base_salary)s);
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
        if data['base_salary'] < 400:
            flash("minimum base salary is 400")
            is_valid = False
        return is_valid
    
    @classmethod
    def delete(cls, data):
        query = """
        delete from employees where id=%(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def edit(cls, data):
        query = """
        UPDATE employees SET first_name = %(first_name)s, last_name = %(last_name)s, cin= %(cin)s , function = %(function)s, base_salary= %(base_salary)s
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
    