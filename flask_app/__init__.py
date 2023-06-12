from flask import Flask
app = Flask(__name__)
app.secret_key = "shhhh this a secret key !!!"
DATABASE = "py_project"