import math
from application.models import User
from flask import json
import datetime as datetime
import pytest
from application.models import PredictionHistory
from application import db,app

# Validity Testing
# Test register
def test_register(client):
    response = client.post('/api/register', json={'username': 'test', 'password': '123'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'id' in data

    with app.app_context():
        user = User.query.filter_by(username='test').first()
        if user:
            db.session.delete(user)
            db.session.commit()
# Validity Testing
def test_api_login(client):
    test_user = {"username": "testuser", "password": "testpass"}
    response = client.post("/api/register", json=test_user)
    assert response.status_code == 200

    login_response = client.post("/api/login", json=test_user)
    assert login_response.status_code == 200
    assert b"Login successful" in login_response.data

    with app.app_context():
        user = User.query.filter_by(username='testuser').first()
        if user:
            db.session.delete(user)
            db.session.commit()

# Validity Testing
# Test if page is rendering
def test_index_page(client):
    res = client.get("/index")
    assert res.status_code == 200
    
    
import json
# Expected Failure
# API Testing when registering duplcate usernames
# Expected failure when username is not unique
def test_duplicate_user_registration(client):
    user_data = {"username": "duplicateUser", "password": "testpass"}

    response = client.post('/api/register', json=user_data)
    assert response.status_code == 200
    # Attempt to register again with the same username
    duplicate_response = client.post('/api/register', json=user_data)
    assert duplicate_response.status_code == 400
    # Cleanup
    with app.app_context():
        User.query.filter_by(username=user_data["username"]).delete()
        db.session.commit()

    
# Validity Testing and Consistency testing
# Test if model 1 and 2 is predicting as intended
import json
from io import BytesIO
import base64
def test_model1_predict(client):
    
    test_user = {"username": "testmodel1", "password": "12345"}
    response = client.post("/api/register", json=test_user)
    assert response.status_code == 200

    login_response = client.post("/api/login", json=test_user)
    assert login_response.status_code == 200
    assert b"Login successful" in login_response.data
    with open('./tests/testImage.jpg', "rb") as image_file:
        image_data=base64.b64encode(image_file.read()).decode('utf-8')
    data = {
        'model_selection': 'Model1_Large',
        'image': image_data
    }
    predict_response = client.post('/api/predict', json=data)
    assert predict_response.status_code == 200
    
    response_data = predict_response.get_json()
    assert 'predicted_class' in response_data and 'confidence' in response_data
    
    with app.app_context():
        user = User.query.filter_by(username='testmodel1').first()
        if user:
            db.session.delete(user)
            db.session.commit()
            

def test_model2_predict(client):
    
    test_user = {"username": "testmodel2", "password": "12345"}
    response = client.post("/api/register", json=test_user)
    assert response.status_code == 200

    login_response = client.post("/api/login", json=test_user)
    assert login_response.status_code == 200
    assert b"Login successful" in login_response.data
    with open('./tests/testImage.jpg', "rb") as image_file:
        image_data=base64.b64encode(image_file.read()).decode('utf-8')
    data = {
        'model_selection': 'Model2_Small',
        'image': image_data
    }
    predict_response = client.post('/api/predict', json=data)
    assert predict_response.status_code == 200
    
    response_data = predict_response.get_json()
    assert 'predicted_class' in response_data and 'confidence' in response_data
    
    with app.app_context():
        user = User.query.filter_by(username='testmodel2').first()
        if user:
            db.session.delete(user)
            db.session.commit()


# Range testing
# Testing prediction with empty image
def test_predict_with_empty_image(client):
    
    test_user = {"username": "testuser31", "password": "12345"}
    response = client.post("/api/register", json=test_user)
    assert response.status_code == 200

    login_response = client.post("/api/login", json=test_user)
    assert login_response.status_code == 200
    assert b"Login successful" in login_response.data
    
    #Empty file
    empty_image_data = base64.b64encode(b'').decode('utf-8')
    data = {
        'model_selection': 'Model1_Large',
        'image': empty_image_data
    }
    predict_response = client.post('/api/predict', json=data)
    assert predict_response.status_code == 400 
    response_data = predict_response.get_json()
    assert 'error' in response_data

    with app.app_context():
        user = User.query.filter_by(username='testuser31').first()
        if user:
            db.session.delete(user)
            db.session.commit()
            
# Range testing
# Testing prediction with fake images
def test_predict_with_fake_image(client):
    
    test_user = {"username": "testuser32", "password": "12345"}
    response = client.post("/api/register", json=test_user)
    assert response.status_code == 200

    login_response = client.post("/api/login", json=test_user)
    assert login_response.status_code == 200
    assert b"Login successful" in login_response.data
    
    #Empty file
    fake_image_data = base64.b64encode(b'Fake').decode('utf-8')
    data = {
        'model_selection': 'Model2_Small',
        'image': fake_image_data
    }
    predict_response = client.post('/api/predict', json=data)
    assert predict_response.status_code == 500 
    response_data = predict_response.get_json()
    assert 'error' in response_data

    with app.app_context():
        user = User.query.filter_by(username='testuser32').first()
        if user:
            db.session.delete(user)
            db.session.commit()
            
            


