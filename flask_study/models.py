from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    classOf = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    
    def __init__(self, classOf, email, username, password):
        self.classOf = classOf
        self.email = email
        self.username = username
        self.password = password
    

    def set_classOf(self, classOf):
        self.classOf = classOf


    def set_email(self, email):
        self.email = email

    
    def set_username(self, username):
        self.username = username


    def set_password(self, password):
        self.password = password
        