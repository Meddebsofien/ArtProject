from django.shortcuts import render

from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Forum
from .forms import ForumForm

class ForumListView(ListView):
    model = Forum
    template_name = 'forum-list.html' 
    context_object_name = 'forums'

class CreateForumView(CreateView):
    model = Forum
    template_name = 'forum-create.html'  
    form_class = ForumForm  
    success_url = reverse_lazy('forum-list')  

    def form_valid(self, form):
        forum = form.save(commit=False)  # Ne pas sauvegarder tout de suite
        forum.owner = self.request.user  # Associer le propriétaire
        forum.save()  # Ensuite, sauvegarder le forum
        return super().form_valid(form)