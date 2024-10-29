from django.db import models
from django.conf import settings  # Ajoutez ceci
# Remplacez l'importation de User par settings.AUTH_USER_MODEL
# from django.contrib.auth.models import User  # Supprimez cette ligne

class Forum(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 

    def __str__(self):
        return self.title
