# models.py in your app where Reclamation and Feedback are defined

from django.conf import settings  # This imports the settings file to get the user model
from django.db import models
from user.models import CustomUser  # Update with your actual custom user model name



class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Using settings.AUTH_USER_MODEL
    rating = models.IntegerField(default=3)  # Add a rating field
    comment = models.TextField()

    def __str__(self):
        return f'Feedback {self.id} - {self.rating}'
