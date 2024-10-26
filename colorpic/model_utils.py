# myapp/model_utils.py

from joblib import load
import os

def load_keras_model():
    #model_path = "C:\\Users\\Sofyen Meddeb\\Desktop\\PythonProject\\SaveModel\\model.joblib"
    model_path ="C:\\Users\\betech.tn\\OneDrive\\Bureau\\validationDjango\\ArtProject\\SaveModel\\model.joblib"
    model = load(model_path)
    return model
