from flask_app import app

from flask_app.controllers import entreprises
from flask_app.controllers import payslips
from flask_app.controllers import employees,tickets

if __name__ == '__main__':
    app.run(debug =True)