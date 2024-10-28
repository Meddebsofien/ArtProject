from django.db import models
import datetime
import os

from user.models import CustomUser
def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow , old_filename)
    return os.path.join("uploads/", filename)
class Publication(models.Model):
    titre = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to=filepath) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='publications')

    def __str__(self):
        return f"{self.titre} by {self.user.username}"

class Commentaire(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='commentaires')
    contenu = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='commentaires')

    def __str__(self):
        return f"Commentaire sur {self.publication.titre} by {self.user.username}"