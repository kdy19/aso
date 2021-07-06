from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo

import datetime


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    index = db.Column(db.Integer, auto_inrement=True, primary_key=True)
    classOf = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    accept = db.Column(db.Boolean, default=False)
    
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


class Refer(db.Model):
    __tablename__ = 'refer'

    index = db.Column(db.Integer, auto_increment=True, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    subject = db.Column(db.String(256), nullable=False)
    content = db.Column(db.String(8192), nullable=False)
    fileName = db.Column(db.String(512), default='')
    fileHash = db.Column(db.String(512), default='')
    write_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    hidden = db.Column(db.Boolean, default=True)

    def __init__(self):
        pass


    def set_username(self, username):
        self.username = username
    

    def set_subject(self, subject):
        self.subject = subject


    def set_content(self, content):
        self.content = content


    def set_fileName(self, fileName):
        self.fileName = fileName

    
    def set_fileHash(self, fileHash):
        self.fileHash = fileHash


class Notice(db.Model):
    __tablename__ = 'notice'

    index = db.Column(db.Integer, auto_increment=True, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    subject = db.Column(db.String(256), nullable=False)
    content = db.Column(db.String(8192), nullable=False)
    fileName = db.Column(db.String(512), default='')
    fileHash = db.Column(db.String(512), default='')
    write_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    hidden = db.Column(db.Boolean, default=True)

    def __init__(self):
        pass


    def set_username(self, username):
        self.username = username
    

    def set_subject(self, subject):
        self.subject = subject


    def set_content(self, content):
        self.content = content


    def set_fileName(self, fileName):
        self.fileName = fileName

    
    def set_fileHash(self, fileHash):
        self.fileHash = fileHash