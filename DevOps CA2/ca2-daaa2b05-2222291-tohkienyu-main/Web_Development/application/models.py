from application import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash,generate_password_hash
from datetime import datetime

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String,unique=True,nullable=False)
    password = db.Column(db.String, nullable=False)
    
    def checkPassword(self,password):
        return self.password == password
    
class PredictionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model_used = db.Column(db.String(255),nullable=False)
    image_name = db.Column(db.String(255), nullable=False)
    predicted_class = db.Column(db.String(255), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)