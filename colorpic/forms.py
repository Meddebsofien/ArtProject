# your_app/forms.py

from django import forms
from .models import Reclamation, Feedback

# forms.py
from django import forms
from .models import Reclamation

class ReclamationForm(forms.ModelForm):
    class Meta:
        model = Reclamation
        fields = ['description', 'status']  # Assurez-vous que ces champs sont inclus



class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comment']  # Only include the fields you want users to fill out


class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Select Image', required=True)
