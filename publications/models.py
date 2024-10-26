from django.db import models
import datetime
import os
def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow , old_filename)
    return os.path.join("uploads/", filename)
class Publication(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to=filepath) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.titre

