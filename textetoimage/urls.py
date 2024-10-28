from django.urls import path
from .views import prompt_form, generate_image

urlpatterns = [
    path('promptext/', prompt_form, name='promptext'),  # Page de formulaire
    path('generate-image/', generate_image, name='generate_image'),  # Génération de l'image
]
