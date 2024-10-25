# colorpic/views.py

from django.http import JsonResponse
import matplotlib.pyplot as plt
from django.views import View
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from .model_utils import load_keras_model
import numpy as np
import cv2
import os

def ExtractTestInput(image):
    # Redimensionner l'image à 224x224 pixels
    img_resized = cv2.resize(image, (224, 224))
    # Convertir l'image en niveaux de gris
    img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    # Ajouter une dimension pour le canal (shape: (224, 224, 1))
    img_l_reshaped = np.expand_dims(img_gray, axis=-1)
    # Ajouter une dimension pour le lot (shape: (1, 224, 224, 1))
    img_l_reshaped = np.expand_dims(img_l_reshaped, axis=0)
    return img_l_reshaped


class ColorizationView(View):
    model = load_keras_model()

    def get(self, request):
        return render(request, 'upload.html')  # Render the upload form

    def post(self, request):
        if 'image' not in request.FILES:
            return JsonResponse({'error': 'No image provided'}, status=400)

        image_file = request.FILES['image']
        
        # Lire l'image depuis le fichier
        img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Vérifiez si l'image a été lue correctement
        if img is None:
            return JsonResponse({'error': 'Failed to read image'}, status=400)

        # Traiter l'image avec ExtractTestInput
        img_l_reshaped = ExtractTestInput(img)

        # Faire la prédiction
        Prediction_5 = self.model.predict(img_l_reshaped)
        Prediction_5 = Prediction_5 * 128
        Prediction_5 = Prediction_5.reshape(224, 224, 2)

        # Afficher l'image originale, la prédiction, etc.
        plt.figure(figsize=(30, 20))
        plt.subplot(5, 5, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
        img_gray_rgb = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)
        img_gray_rgb = cv2.resize(img_gray_rgb, (224, 224))
        plt.imshow(img_gray_rgb)
        plt.subplot(5, 5, 2)
        img_lab = cv2.cvtColor(img_gray_rgb, cv2.COLOR_RGB2Lab)
        img_lab[:, :, 1:] = Prediction_5
        img_colorized = cv2.cvtColor(img_lab, cv2.COLOR_Lab2RGB)
        plt.title("Predicted Image")
        plt.imshow(img_colorized)
        plt.subplot(5, 5, 3)
        plt.title("Ground truth")
        plt.imshow(img_rgb)

        # Enregistrer le plot si besoin
        plt.savefig('media/colorized_image.png')  # Spécifiez le chemin de sauvegarde
 # Enregistrer l'image colorisée
      #  save_path = os.path.join(settings.MEDIA_ROOT, 'colorized_image.png')
       # cv2.imwrite(save_path, img_colorized)

        
    # Passez l'URL de l'image au contexte
        image_url = '/media/colorized_image.png'
        return render(request, 'upload.html', {'image_url': image_url})