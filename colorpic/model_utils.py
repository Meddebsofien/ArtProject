# myapp/model_utils.py

from joblib import load
import os

def load_keras_model():
    model_path = "C:\\Users\\Admin\\Documents\\Django\\ArtProject\\SaveModel\\model.joblib"
    model = load(model_path)
    return model
