from application import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash,generate_password_hash
class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model = db.Column(db.String)
    year = db.Column(db.Integer)
    transmission = db.Column(db.String)
    mileage = db.Column(db.Integer)
    tax = db.Column(db.Integer)
    mpg = db.Column(db.Float) 
    engineSize = db.Column(db.Float) 
    prediction = db.Column(db.Integer)
    predicted_on = db.Column(db.DateTime, nullable=False) 
    userID = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String,unique=True,nullable=False)
    password = db.Column(db.String, nullable=False)
    
    def checkPassword(self,password):
        return self.password == password