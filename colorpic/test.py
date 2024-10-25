import pytest
from .model_utils import load_keras_model  # Update to match the function name

def test_load_keras_model():
    # Path to your model file
    model_path = "C:\\Users\\Sofyen Meddeb\\Desktop\\PythonProject\\SaveModel\\model.joblib"
    
    # Call the loading function
    model = load_keras_model()  # Call the updated function
    
    # Check that the model is loaded correctly
    assert model is not None
