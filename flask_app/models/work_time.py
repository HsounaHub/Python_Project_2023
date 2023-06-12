from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Work_time :
    def __init__(self,data):
        self.id = data['id']
        self.employee_id=data['employee_id']
        self.month=data['month']
        self.work_hours=data['work_hours']
        self.login_time=data['login_time']
        self.logout_time=data['logout_time']

    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * FROM work_time WHERE employee_id = %(employee_id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def new(cls, data):
        query = """
        INSERT INTO work_time (employee_id,work_hours) 
        VALUES (%(employee_id)s,0);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def login(cls, data):
        query = """
        UPDATE work_time
        SET login_time = %(login_time)s
        WHERE employee_id = %(employee_id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def logout(cls, data):
        query = """
        UPDATE work_time
        SET work_hours = %(work_hours)s, logout_time = %(logout_time)s
        WHERE employee_id = %(employee_id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)