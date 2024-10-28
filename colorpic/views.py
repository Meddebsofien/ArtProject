# colorpic/views.py

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import  Feedback
from .forms import FeedbackForm
import matplotlib.pyplot as plt
from django.views import View
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from .model_utils import load_keras_model
import numpy as np
from django.contrib import messages  # Ajoutez ceci
import requests
from django.http import JsonResponse, HttpResponse
from huggingface_hub import HfApi
from django.contrib.auth.decorators import login_required

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

# your_app/views.py


# Liste des réclamations




# Création d'un feedback
from django.shortcuts import render, redirect, get_object_or_404
from .models import Feedback
from .forms import FeedbackForm

# Création d'un feedback
@login_required
def feedback_create(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Attach the logged-in user
            feedback.rating = get_sentiment_analysis(feedback.comment)  # Get rating from sentiment analysis
            feedback.save()
            messages.success(request, "Feedback submitted successfully!")
            return redirect('feedback_list')  # Redirect to the feedback list page
    else:
        form = FeedbackForm()

    return render(request, 'feedback_form.html', {'form': form})
# Détails d'un feedback
def feedback_detail(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    return render(request, 'your_app/feedback_detail.html', {'feedback': feedback})

# Mise à jour d'un feedback
def feedback_update(request, feedback_id):
    # Récupérer le feedback à mettre à jour
    feedback = get_object_or_404(Feedback, id=feedback_id)

    if request.method == 'POST':
        # Créer le formulaire avec les données POST et l'instance existante
        form = FeedbackForm(request.POST, instance=feedback)
        
        if form.is_valid():
            # Enregistrer le feedback mis à jour
            form.save()
            # Rediriger vers la liste des feedbacks avec un message de succès
            return redirect('feedback_list')  # Redirige vers la liste des feedbacks
    else:
        # Initialiser le formulaire avec l'instance existante
        form = FeedbackForm(instance=feedback)

    # Rendre le template avec le formulaire
    return render(request, 'feedback_update.html', {'form': form})
# Suppression d'un feedback



def feedback_delete(request, feedback_id):
    # Récupération de l'objet feedback ou renvoie une 404 si non trouvé
    feedback = get_object_or_404(Feedback, id=feedback_id)
    
    # Suppression du feedback
    feedback.delete()
    
    # Redirection vers la liste des feedbacks
    return redirect('feedback_list')  # Assurez-vous que 'feedback_list' est le nom correct de votre URL de liste des feedbacks
# Liste des feedbacks





HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
API_TOKEN = "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"  # Remplacez par votre token

def get_sentiment_analysis(text):
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    payload = {"inputs": text}

    response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
    result = response.json()
    
    if response.status_code == 200 and result:
        # Récupérer le score pour "positive" et "negative"
        for label in result[0]:
            if label['label'] == 'POSITIVE':
                return 5  # Attribuer une note élevée si sentiment positif
            elif label['label'] == 'NEGATIVE':
                return 2  # Note plus basse pour un sentiment négatif
    return 3  # Note neutre si aucune donnée n'est retournée
@login_required
def feedback_list(request):
    feedbacks = Feedback.objects.all()

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.rating = get_sentiment_analysis(feedback.feedback_text)  # Analyse de sentiment
            feedback.user = request.user  # Associer le feedback à l'utilisateur connecté
            feedback.save()
            return redirect('feedback_list')  # Redirection pour actualiser la page avec le nouveau feedback
    else:
        form = FeedbackForm()

    context = {
        'feedbacks': feedbacks,
        'form': form,
    }
    return render(request, 'feedback_list.html', context)