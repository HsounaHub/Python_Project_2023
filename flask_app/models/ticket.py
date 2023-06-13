from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Tickets:
    def __init__(self,data):
        self.id = data['id']
        self.title=data['title']
        self.object= data['object']
        self.closed_time=data['closed_date']
        self.status= data['status']
        self.employee_id=data['employee_id']
        self.entreprise_id = data['entreprise_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add_ticket(cls, data):
        query = """
        INSERT INTO tickets (title,object,status,employee_id,entreprise_id)
        VALUES (%(title)s,%(object)s,%(status)s,%(employee_id)s,%(entreprise_id)s);
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
        UPDATE tickets SET  title=%(title)s, object=%(object)s,closed_date=%(closed_date)s,status=%(status)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_by_id_enterprise_id(cls, data):
        query = """
        SELECT * FROM tickets WHERE entreprise_id = %(entreprise_id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        ent = []
        for row in result:
            ent.append(cls(row))
        return ent


    @classmethod
    def get_by_id_employee_id(cls, data):
        query = """
        SELECT * FROM tickets WHERE employee_id = %(employee_id)s;
        """
        result = connectToMySQL(DATABASE).query_db(query,data)
        emp = []
        for row in result:
            emp.append(cls(row))
        return emp