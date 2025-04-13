from application import app
from flask import render_template,request,flash,url_for,redirect
from application.forms import PredictionForm,LoginForm,RegisterForm
from application import ai_model
from application import db
from application.models import Entry,User
from datetime import datetime
from sklearn.preprocessing import LabelEncoder
from flask_login import login_user,current_user,logout_user,login_required
import pickle
from joblib import load
import numpy as np
import pandas as pd

with open('./application/static/encoder.pkl','rb') as encoderFile:
    encoder = pickle.load(encoderFile)
    # encoder = load(encoderFile)
with open('./application/static/encoder2.pkl','rb') as encoderFile2:
    encoder2 = pickle.load(encoderFile2)
    # encoder2 = load(encoderFile2)
    
with open('./application/static/scaler.pkl','rb') as scaler:
    minMaxScaler = pickle.load(scaler)
    # encoder2 = load(encoderFile2)
with open('./application/static/featureNames.pkl','rb') as featureNameFile:
    feature_names = pickle.load(featureNameFile)
    # encoder2 = load(encoderFile2)




print(encoder.classes_)
print(encoder2.classes_)



#Handles http://127.0.0.1:5000/
# @app.route('/')
# @app.route('/index')
# @app.route('/home')
# ## Remove this
# @login_required
# def index_page():
#     form1 = PredictionForm()
#     return render_template("index.html", form=form1, title="Enter Ford Car Parameters",entries=get_entries())

@app.route('/')
@app.route('/index')
@app.route('/home')
## Remove this
def index_page():
    form3 = PredictionForm()
    return render_template("index.html", title="Home",form=form3,current_page="home")


@app.route('/predictform')
## Remove this
@login_required
def prediction_page():
    form1 = PredictionForm()
    return render_template("predictform.html", form=form1, title="Enter Ford Car Parameters",entries=get_entries())

@app.route('/history')
## Remove this
@login_required
def showPredictionTable():
    return render_template("history.html", title="Prediction Table",entries=get_entries())

@app.route("/predict", methods=['GET','POST'])
@login_required
def predict():
    form = PredictionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            model = form.model.data
            year = int(form.year.data)
            transmission = form.transmission.data
            mileage = int(form.mileage.data)
            tax = int(form.tax.data)
            mpg = float(form.mpg.data)
            engineSize = float(form.engineSize.data)

            encodedModel = encoder.transform([model])
            encodedTransmission = encoder2.transform([transmission])
            print(model)
            # print(encodedModel)
            X = pd.DataFrame([[encodedModel[0], year, encodedTransmission[0],mileage, tax,mpg,engineSize]],columns=feature_names)
            print(X)
            X_scaled = minMaxScaler.transform(X)
            resultScaled = ai_model.predict(X_scaled)
            print(resultScaled)
            new_entry = Entry(model=model,
                                year=year,
                                transmission=transmission, 
                                mileage = mileage,
                                tax=tax,
                                mpg = mpg,
                                engineSize=engineSize,
                                prediction=int(resultScaled[0]),
                                predicted_on=datetime.utcnow(),
                                userID = current_user.id)
            add_entry(new_entry) 
            flash(f"Prediction: {resultScaled[0]}","success") 
        else:
            flash("Error, cannot proceed with prediction","danger")
    return render_template("predictform.html", title="Enter Ford Car Parameters", form=form, index=True,entries=get_entries()) 

def add_entry(new_entry):
    try:
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.id
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")

def get_entries():
    try:
        if current_user.is_authenticated:
            entries = Entry.query.filter_by(userID=current_user.id)
        # entries = Entry.query.all() # version 2
        # entries = db.session.execute(db.select(Entry).order_by(Entry.id)).scalars()
        return entries
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")
        return 0
    
# Added in Practical 5
def remove_entry(id):
    try:
        # entry = Entry.query.get(id) # version 2
        entry = db.get_or_404(Entry, id)
        db.session.delete(entry)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")
        return 0
    
@app.route('/remove', methods=['POST'])
def remove():
    form = PredictionForm()
    req = request.form
    id = req["id"]
    remove_entry(id)
    return render_template("history.html", title="Enter Ford Car Parameters",form=form, entries = get_entries(), index=True) 

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('prediction_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user and user.checkPassword(form.password.data):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('prediction_page'))
        
        else:
            flash('Login unsucessful. Please enter correct username or password.','danger')
    return render_template('login.html',title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Log out successful','success')
    return redirect(url_for('login'))

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('prediction_page'))
    form = RegisterForm()
    print(form.data)
    if form.validate_on_submit():
        existingUser = User.query.filter_by(username=form.username.data).first()
        
        if existingUser:
            flash('Username already exists. Please choose another username','danger')
            
        else:
            newUser = User(username=form.username.data, password = form.password.data)
            try:
                # hashedPassword = generate_hash(form.password.data)
                db.session.add(newUser)
                db.session.commit()
                flash('Registration successful. Proceed to login.','success')
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash(f'Error:{e}','danger')
        
    return render_template('register.html',title='Register', form=form)


# Test API
from flask import json, jsonify
#API: add entry
@app.route("/api/register", methods=['POST'])
def api_register():
    #retrieve the json file posted from client
    data = request.get_json()
    #retrieve each field from the data
    username = data['username']
    password = data['password']
    print(data)
    #create an Entry object store all data for db action
    new_entry = User( username=username, password=password)
    #invoke the add entry function to add entry
    result = add_entry(new_entry)
    #return the result of the db action
    return jsonify({'id':result})


#API: add predict entry
@app.route("/api/predict", methods=['POST'])
def api_addPredict():
    #retrieve the json file posted from client
    data = request.get_json()
    #retrieve each field from the data
    model = data['model']
    year = data['year']
    transmission = data['transmission']
    mileage = data['mileage']
    tax = data['tax']
    mpg = data['mpg']
    engineSize = data['engineSize']
    prediction = data['prediction']
    userID = data['userID']
    print(data)
    #create an Entry object store all data for db action
    new_entry = Entry(model=model, year=year,transmission=transmission,mileage=mileage,tax=tax,mpg=mpg,engineSize=engineSize,prediction=prediction,predicted_on=datetime.utcnow(),userID=userID)
    #invoke the add entry function to add entry
    result = add_entry(new_entry)
    #return the result of the db action
    return jsonify({'id':result})

#API delete entry
@app.route("/api/delete/<id>", methods=['GET'])
def api_delete(id):
    entry = remove_entry(int(id))
    return jsonify({'result':'ok'})
