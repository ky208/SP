from application import app
from flask import render_template, request, flash
from flask_cors import CORS, cross_origin
from tensorflow.keras.preprocessing import image
from PIL import Image, ImageOps
import numpy as np
import re
from application import db
import base64
from io import BytesIO
# from tensorflow.keras.datasets.mnist import load_data
import json
import numpy as np
import requests
import pathlib, os
from flask_login import login_user,current_user,logout_user,login_required
from application.forms import LoginForm,RegisterForm
from flask import render_template,request,flash,url_for,redirect
from application.models import User,PredictionHistory
from datetime import datetime
from werkzeug.utils import secure_filename

def make_prediction(url,instances):
    data = json.dumps({"signature_name": "serving_default","instances": instances.tolist()}) #see [C]
    headers = {"content-type": "application/json"}
    json_response = requests.post(url, data=data, headers=headers)
    print(json_response.text)
    predictions = json.loads(json_response.text)['predictions']
    
    prediction_index = np.argmax(predictions[0])
    predicted_confidence = max(predictions[0])
    return prediction_index,float(predicted_confidence)
#Handles http://127.0.0.1:5000/
@app.route('/')
@app.route('/index')
@app.route('/home')
def index_page():
    return render_template('index.html')

@app.route('/predict',methods=['GET'])
@login_required
def predict_page():
    return render_template('predict.html')
    
@app.route("/predict", methods=['POST'])
@login_required
@cross_origin(origin='*', headers=['Content-Type', 'Authorization'])
def predict():
    classes = ['Bean','Bitter_Gourd','Bottle_Gourd','Brinjal','Broccoli','Cabbage','Capsicum','Carrot','Cauliflower','Cucumber','Papaya','Potato','Pumpkin','Radish','Tomato']
    modelSelect = request.form['model_selection']
    if modelSelect == 'Model1_Large':
        target_size = (128, 128)
        model_url = 'https://dlmodelapp-ca2-dl1j.onrender.com/v1/models/Model1_Large:predict'
    elif modelSelect == 'Model2_Small':
        target_size = (31, 31)
        model_url = 'https://dlmodelapp-ca2-dl1j.onrender.com/v1/models/Model2_Small:predict'
    else:
        flash('Invalid model selection', 'danger')
        return redirect(url_for('predict_page'))
    
    try:
        file = request.files.get('image')
        if file:
            filename = secure_filename(file.filename)
            img = Image.open(file.stream).convert('RGB')
            img = img.convert('L')
            img = img.resize(target_size)
            img_array = np.array(img) / 255.0
            img_array = img_array.reshape(1, *target_size, 1)
            
            predicted_index,predicted_confidence = make_prediction(model_url, img_array)
            predicted_class = classes[predicted_index]

            # Save prediction result along with confidence to PredictionHistory
            new_prediction = PredictionHistory(
                model_used=modelSelect,
                image_name=filename,
                predicted_class=predicted_class,
                confidence=predicted_confidence,  # Assuming you have a way to calculate this
                date=datetime.utcnow(),
                user_id=current_user.id
            )
            db.session.add(new_prediction)
            db.session.commit()
            
            flash('Prediction saved successfully!', 'success')
            return render_template('predict.html', prediction_result=predicted_class, confidence=predicted_confidence)
        else:
            flash('No file selected or invalid file format.', 'danger')
            return redirect(url_for('predict_page'))
    except Exception as e:
        flash(f'Error during prediction: {e}', 'danger')
        return redirect(url_for('predict_page'))


@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('predict_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        if user and user.checkPassword(form.password.data):
            login_user(user)
            flash('Login successful', 'success')
            return redirect(url_for('predict_page'))
        
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
        return redirect(url_for('predict_page'))
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


@app.route('/predictionHistory')
@login_required
def prediction_history():
    classes = ['Bean', 'Bitter_Gourd', 'Bottle_Gourd', 'Brinjal', 'Broccoli', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Cucumber', 'Papaya', 'Potato', 'Pumpkin', 'Radish', 'Tomato']
    models = ['Model1_Large', 'Model2_Small']

    model_filter = request.args.get('model', 'all')
    class_filter = request.args.get('class', 'all')
    search_query = request.args.get('search', '')

    predictions_query = PredictionHistory.query.filter_by(user_id=current_user.id)
    if model_filter != 'all':
        predictions_query = predictions_query.filter(PredictionHistory.model_used == model_filter)
    if class_filter != 'all':
        predictions_query = predictions_query.filter(PredictionHistory.predicted_class == class_filter)

    if search_query:
        predictions_query = predictions_query.filter(
            db.or_(
                PredictionHistory.model_used.ilike(f'%{search_query}%'),
                PredictionHistory.predicted_class.ilike(f'%{search_query}%'),
                PredictionHistory.image_name.ilike(f'%{search_query}%')
            )
        )

    user_predictions = predictions_query.all()

    return render_template('predictionHistory.html', predictions=user_predictions, unique_models=models, unique_classes=classes, model_filter=model_filter, class_filter=class_filter)



@app.route('/deletePrediction/<int:prediction_id>')
@login_required
def delete_prediction(prediction_id):
    prediction_to_delete = PredictionHistory.query.get_or_404(prediction_id)
    if prediction_to_delete.user_id != current_user.id:
        flash('Unauthorized to delete this record.', 'danger')
        return redirect(url_for('prediction_history'))
    
    db.session.delete(prediction_to_delete)
    db.session.commit()
    flash('Prediction deleted successfully!', 'success')
    return redirect(url_for('prediction_history'))



# Testing APIs

# Test API
from flask import json, jsonify

def add_entry(new_entry):
    try:
        db.session.add(new_entry)
        db.session.commit()
        return new_entry.id
    except Exception as error:
        db.session.rollback()
        flash(error,"danger")
#API: add entry
@app.route("/api/register", methods=['POST'])
def api_register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    print(data)
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400
    new_entry = User(username=username, password=password)
    result = add_entry(new_entry)
    return jsonify({'id': result})


#API: login
@app.route("/api/login", methods=['POST'])
def api_login():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user is None or not user.checkPassword(password):
        return jsonify({'error': 'Invalid username or password'}), 401

    login_user(user)
    return jsonify({'message': 'Login successful', 'username': user.username}), 200


from flask import request, jsonify, current_app
from flask_login import login_required
import base64
from io import BytesIO
from PIL import Image
import numpy as np

@app.route("/api/predict", methods=['POST'])
@login_required
def api_predict():
    data = request.json
    modelSelect = data.get('model_selection')
    image_data = data.get('image')
    if not modelSelect or not image_data:
        return jsonify({'error': 'Missing model selection or image data'}), 400

    if modelSelect == 'Model1_Large':
        target_size = (128, 128)
        model_url = 'https://dlmodelapp-ca2-dl1j.onrender.com/v1/models/Model1_Large:predict'
    elif modelSelect == 'Model2_Small':
        target_size = (31, 31)
        model_url = 'https://dlmodelapp-ca2-dl1j.onrender.com/v1/models/Model2_Small:predict'
    else:
        return jsonify({'error': 'Invalid model selection'}), 400

    try:
        # Decode the image
        img = Image.open(BytesIO(base64.b64decode(image_data)))
        img = img.convert('L') 
        img = img.resize(target_size)
        img_array = np.array(img) / 255.0
        img_array = img_array.reshape(1, *target_size, 1)
        
        predicted_index, predicted_confidence = make_prediction(model_url, img_array)
        predicted_class = ['Bean','Bitter_Gourd','Bottle_Gourd','Brinjal','Broccoli','Cabbage','Capsicum','Carrot','Cauliflower','Cucumber','Papaya','Potato','Pumpkin','Radish','Tomato'][predicted_index] 

        return jsonify({
            'predicted_class': predicted_class,
            'confidence': predicted_confidence
        })
    except Exception as e:
        current_app.logger.error(f'Prediction error: {e}')
        return jsonify({'error': 'Error processing prediction'}), 500


