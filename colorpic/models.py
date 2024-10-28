# models.py in your app where Reclamation and Feedback are defined

from django.conf import settings  # This imports the settings file to get the user model
from django.db import models
from user.models import CustomUser  # Update with your actual custom user model name

class Reclamation(models.Model):
    STATUS = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('resolu', 'Résolu'),
    ]
    SERVICE_CHOICES = [
        ('generate_image', 'Generate Image from Text'),
        ('colorize_image', 'Colorize Image'),
        ('autres', 'Autres'),
    ]

    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default='en_attente')
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES, default='autres')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'Reclamation {self.id} - {self.status}'

class Feedback(models.Model):
    reclamation = models.ForeignKey(Reclamation, on_delete=models.CASCADE, related_name='feedbacks', null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Using settings.AUTH_USER_MODEL
    rating = models.IntegerField(default=3)  # Add a rating field
    comment = models.TextField()

    def __str__(self):
        return f'Feedback {self.id} - {self.rating}'
