# your_app/forms.py

from django import forms
from .models import  Feedback

# forms.py
from django import forms





class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comment']  # Only include the fields you want users to fill out


class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Select Image', required=True)
