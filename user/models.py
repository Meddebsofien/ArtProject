from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class CustomUser(AbstractUser):
    # Additional fields
    photo = models.ImageField(upload_to='photo/', null=True, blank=True)
    
    ABONNEMENT_CHOICES = [
        ('pas_abonnement', 'Pas d\'abonnement'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]
    abonnement = models.CharField(max_length=15, choices=ABONNEMENT_CHOICES, default='pas_abonnement')

    def __str__(self):
        return self.username

class PasswordReset(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Use the custom model here
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_when = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset for {self.user.username} at {self.created_when}"
