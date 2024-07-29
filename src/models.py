from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    az_title = db.Column(db.String)
    en_title = db.Column(db.String)
    az_content = db.Column(db.String)
    en_content = db.Column(db.String)
    image = db.Column(db.String)

    def __init__(self, az_title, en_title, az_content, en_content, image):
        self.az_title = az_title
        self.en_title = en_title
        self.az_content = az_content
        self.en_content = en_content
        self.image = image
