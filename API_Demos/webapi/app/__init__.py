from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
#creating the db based on the config file
db = SQLAlchemy(app)


from app import views, models
