# reclamation/models.py
from django.db import models
from user.models import CustomUser

class Reclamation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reclamations')
    titre = models.CharField(max_length=100)
    description = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20,
        choices=[('Ouverte', 'Ouverte'), ('En cours', 'En cours'), ('Résolue', 'Résolue')],
        default='Ouverte'
    )

    def __str__(self):
        return self.titre

    def get_statut_color(self):
        """Retourne la couleur de fond en fonction du statut"""
        if self.statut == 'Résolue':
            return 'bg-green-500'
        elif self.statut == 'En cours':
            return 'bg-yellow-500'
        return 'bg-red-500'

class Reponse(models.Model):
    reclamation = models.ForeignKey(Reclamation, on_delete=models.CASCADE, related_name='reponses')
    reponse = models.TextField()
    date_reponse = models.DateTimeField(auto_now_add=True)