import json
from keras.models import load_model
import numpy as np
import cv2
import urllib.request
base_url = "http://192.168.0.12:8000"
def model_load(filename):
    """This function loads the .h5 model file for the filename is argument"""
    model = load_model('{}/model/{}.h5'.format(filename, filename))
    return model

def get_image(im_url):
    """This function fetches the image for the given path so that it can be classified"""
    url = base_url + im_url
    url_response = urllib.request.urlopen(url)
    img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, -1)
    img = cv2.resize(img, (100,100))
    img = np.reshape(img, (1,100,100,3))
    return img

def get_labels(filename):
    """This function parses the label file (.txt) as a json file to load the categories for which the model has been trained"""
    path = '{}/model/labels.txt'.format(filename)
    with open(path) as json_file:  
         data = json.load(json_file)
    labels = {}
    names = {}
    for p in data['category']:
        labels[p['index']] = p['id']
        names[p['id']]=p['name']
    return labels, names

def predict_class(img, model, labels, names):
    """This function finally predicts the category for the given image and classifies it while retturning the 
       class ID, class name and the confidence score"""
    p = model.predict(img)
    pred = np.argmax(p, axis=1)
    predicted_id = labels[pred]
    predicted_class = names[predicted_id] 
    confidence = p[0][pred]
    return predicted_id, predicted_class, confidence
#labels, names = get_labels("wtpsth")
#print(labels, names)
