from flask import Flask
from flask_cors import CORS
import pickle
from flask_sqlalchemy import SQLAlchemy
from joblib import dump,load
from flask_login import LoginManager,login_user #pip install flask-login
#create the Flask app
db = SQLAlchemy()

app = Flask(__name__)

CORS(app)

loginManager = LoginManager(app)
loginManager.login_view = 'login'
from application.models import User

def load_user(user_id):
    return User.query.get(int(user_id))

loginManager.user_loader(load_user)

# load configuration from config.cfg
app.config.from_pyfile('config.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# new method for SQLAlchemy version 3 onwards
with app.app_context():
    db.init_app(app)
    # from .models import PredictionHistory
    db.create_all()
    db.session.commit()
    print('Created Database!') 
#AI model file
# joblib_file = "./application/static/ford_Model.pkl"
# # Load from file
# # ai_model = load(joblib_file)
# with open(joblib_file, 'rb') as f:
#     ai_model = pickle.load(f) 
#run the file routes.py
from application import routes