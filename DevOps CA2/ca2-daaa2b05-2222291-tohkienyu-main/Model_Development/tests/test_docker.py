import pytest
import requests
import base64
import json
import numpy as np
from tensorflow.keras.utils import image_dataset_from_directory
from tensorflow.image import resize

## Testing docker

def test_model1_large():
    test = image_dataset_from_directory(directory='./tests/test',color_mode='grayscale',label_mode='categorical',image_size=(128,128))
    # url = 'http://digit_server_CA2:8501/v1/models/Model1_Large:predict' #see [B]
    url = 'https://dlmodelapp-ca2-dl1j.onrender.com/v1/models/Model1_Large:predict'
    X_test = []
    y_test = []

    for images, labels in test:
        X_test.append(images)
        y_test.append(labels)

    X_test = np.concatenate(X_test, axis=0)
    # X_test = np.squeeze(X_test, axis=-1)
    y_test = np.concatenate(y_test, axis=0)

    X_test = np.array(X_test) / 255.0
    # # reshape data to have a single channel
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], X_test.shape[2],1))
    run_model_test(url,X_test,y_test)
    
def test_model2_small():
    test = image_dataset_from_directory(directory='./tests/test',color_mode='grayscale',label_mode='categorical',image_size=(31,31))
    # url = 'http://digit_server_CA2:8501/v1/models/Model2_Small:predict'
    url = 'https://dlmodelapp-ca2-dl1j.onrender.com/v1/models/Model2_Small:predict'
    X_test = []
    y_test = []

    for images, labels in test:
        X_test.append(images)
        y_test.append(labels)

    X_test = np.concatenate(X_test, axis=0)
    # X_test = np.squeeze(X_test, axis=-1)
    y_test = np.concatenate(y_test, axis=0)

    X_test = np.array(X_test) / 255.
    # # reshape data to have a single channel
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], X_test.shape[2],1))
    run_model_test(url,X_test,y_test)
    
    

def make_prediction(url,instances):
    data = json.dumps({"signature_name": "serving_default","instances": instances.tolist()}) #see [C]
    headers = {"content-type": "application/json"}
    json_response = requests.post(url, data=data, headers=headers)
    print(json_response.text)
    predictions = json.loads(json_response.text)['predictions']
    return predictions

def run_model_test(url,X_test,y_test):
    predictions = make_prediction(url,X_test[0:4]) #see [A]
    for i, pred in enumerate(predictions):
        true_label = np.argmax(y_test[i])
        predicted_label = np.argmax(pred)
        assert true_label==predicted_label
