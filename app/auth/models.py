from sqlalchemy.orm import relationship
from sqlalchemy import Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app import db

class Model(db.Model):

    __abstract__  = True

    id = db.Column(Integer, primary_key=True)
    date_created  = db.Column(DateTime, default=func.current_timestamp())
    date_modified = db.Column(DateTime, default=func.current_timestamp(),
                                           onupdate=func.current_timestamp())
 
class User(Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(50))
    email = db.Column(String(100))
    password = db.Column(String(60))#hash with salt

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password                                    