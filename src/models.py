from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, JSON

db = SQLAlchemy()

class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)

class Event(db.Model):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    az_title = Column(String)
    en_title = Column(String)
    az_content = Column(String)
    en_content = Column(String)
    image = Column(String)

    def __init__(self, az_title, en_title, az_content, en_content, image):
        self.az_title = az_title
        self.en_title = en_title
        self.az_content = az_content
        self.en_content = en_content
        self.image = image

class FormSubmission(db.Model):
    __tablename__ = 'form_submission'
    id = Column(Integer, primary_key=True)
    data = Column(JSON)

    def __init__(self, payload):
        self.data = payload

class GalleryImage(db.Model):
    __tablename__ = 'gallery_image'
    id = Column(Integer, primary_key=True)
    image_url = Column(String)

    def __init__(self, image_url):
        self.image_url = image_url
