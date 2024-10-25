import pytest
import numpy as np
from .model_utils import load_keras_model
from .views import ExtractTestInput  # Assurez-vous que l'importation est correcte

def test_extract_test_input():
    # Créer une image d'exemple (par exemple, un tableau NumPy de forme (256, 256, 3))
    test_input = np.random.randint(0, 256, (256, 256, 3), dtype=np.uint8)  # Image aléatoire de 256x256

    # Appeler la fonction
    result = ExtractTestInput(test_input)

    # Vérifiez que la forme de la sortie est correcte
    expected_shape = (255, 255, 3)  # Remplacez par les dimensions correctes
    assert result.shape == expected_shape
