import math
from application.models import User
from flask import json
import datetime as datetime
import pytest
from application.models import Entry
# Registration API Testing
# Passes when unique username is inserted into the database
# Expected failure when username is not unique
# Expected Failure testing and Consistency testing
@pytest.mark.parametrize("entrylist",[
    ['newUser40','123'], 
    ['duplicatedUser','12345'],
    ['duplicatedUser','12345']
])

def test_addUser(client,entrylist,capsys):
    with capsys.disabled():
        #prepare the data into a dictionary
        data1 = { 'username': entrylist[0],
        'password' : entrylist[1],
        }
        #use client object to post
        #data is converted to json
        #posting content is specified
        try:
            response = client.post('/api/register',
                                        data=json.dumps(data1),
                                        content_type="application/json",)
            #check the outcome of the action
            assert response.status_code == 200
            assert response.headers["Content-Type"] == "application/json"
            response_body = json.loads(response.get_data(as_text=True))
            assert response_body["id"] is not None
            print(f"Added Entry: {response_body['id']}")
        except TypeError as e:
            print("Username already exists. Please choose another username.")    
            pytest.xfail("Username must be unique.")
            
        
           
            
#Test adding and removing prediction API in prediction history
# Consistency Testing
@pytest.mark.parametrize("entrylist",[
 ['Puma', 2017, 'Automatic', 20000, 150,57.7,1,26000,1]
])
def test_deletePredictionAPI(client, entrylist, capsys):
    with capsys.disabled():
        data1 = {
            'model': entrylist[0],
            'year': entrylist[1],
            'transmission': entrylist[2],
            'mileage': entrylist[3],
            'tax': entrylist[4],
            'mpg': entrylist[5],    
            'engineSize': entrylist[6],
            'prediction':entrylist[7],
            'userID':entrylist[8]}
        
        response = client.post('/api/predict',data=json.dumps(data1),content_type="application/json")
        response_body = json.loads(response.get_data(as_text=True))
        
        assert response_body["id"]
        id = response_body["id"]
        print(f"Added Entry: {response_body['id']}")
        
        response2 =  client.get(f'/api/delete/{id}')
        ret = json.loads(response2.get_data(as_text=True))
        assert response2.status_code == 200
        assert response2.headers["Content-Type"] == "application/json"
        response2_body = json.loads(response2.get_data(as_text=True))
        assert response2_body["result"] == "ok"
        print(f"Deleted Entry: {response_body['id']}")
        
# Validity Testing
@pytest.mark.parametrize("entrylist",[
 ['Puma', 2017, 'Automatic', 20000, 150,57,1,26000,1],
 ['B-MAX', 2014.2, 'Manual', 20000.0, 145.3,58.7,1,23000,1]
])
#3: Write the test function pass in the arguments
def test_EntryClass(entrylist,capsys):
    with capsys.disabled():
        print(entrylist)
        now = datetime.datetime.utcnow()
        new_entry = Entry( model= entrylist[0],
                            year = entrylist[1],
                            transmission= entrylist[2],
                            mileage = entrylist[3],
                            tax = entrylist[4],
                            mpg = entrylist[5],
                            engineSize = entrylist[6],
                            prediction = entrylist[7],
                            userID = entrylist[8],
                            predicted_on= now)
        
        assert new_entry.model == entrylist[0]
        assert new_entry.year == entrylist[1]
        assert new_entry.transmission == entrylist[2]
        assert new_entry.mileage == entrylist[3]
        assert new_entry.tax == entrylist[4]
        assert new_entry.mpg == entrylist[5]
        assert new_entry.engineSize == entrylist[6]
        assert new_entry.prediction == entrylist[7]
        assert new_entry.userID == entrylist[8]
        assert new_entry.predicted_on == now

#4: Expected Failure Testing
@pytest.mark.xfail(reason="arguments < 0")
@pytest.mark.parametrize("entrylist",[
 ['Puma', -2017, 'Automatic', 20000, 150,57,1,26000,1],
 ['B-MAX', 2014.2, 'Manual', -20000.0, 145.3,58.7,1,-23000,-1],
 ['Galaxy', 0, 'Automatic', -30000, -150,57,1,26000,1],
 ['Puma', 2014.5, 'Manual', 20000.0, 145.3,58.7,-1,23000,1],

])
def test_EntryValidation(entrylist, capsys):
    test_EntryClass(entrylist, capsys)
