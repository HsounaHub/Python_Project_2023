from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Tickets:
    def __init__(self,data):
        self.id = data['id']
        self.object= data['object']
        self.description= data['description']
        self.closed_time=data['closed_time']
        self.status= data['status']
        self.employee_id=data['employee_id']
        self.entreprise_id = data['entreprise_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def add_ticket(cls, data):
        query = """
        INSERT INTO tickets (object,description,closed_time,status,employee_id,entreprise_id)
        VALUES (%(object)s,%(description)s,%(closed_time)s,%(status)s,%(employee_id)s,%(entreprise_id)s);
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT * FROM tickets WHERE id = %(id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])

    @classmethod
    def edit_ticket(cls, data):
        query = """
        UPDATE tickets SET object=%(object)s,description=%(description)s,closed_time=%(closed_time)s,status=%(status)s,employee_id=%(employee_id)s,entreprise_id=%(entreprise_id)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
