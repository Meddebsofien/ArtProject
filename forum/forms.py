# forum/forms.py
from django import forms
from .models import Forum

class ForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['title', 'description']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            return title.strip()  # Enlève les espaces avant et après
        raise forms.ValidationError("Ce champ est requis.")
