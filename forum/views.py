from django.shortcuts import render
import logging
logger = logging.getLogger(__name__)
from django.views.generic import ListView, CreateView, UpdateView
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
        
        forum = form.save(commit=False)
        forum.owner = self.request.user
        forum.save()
        logger.info(f'Forum created: {forum.title} by {forum.owner.username}')
        return super().form_valid(form)

    def form_invalid(self, form):
        print(f'Submitted data: {self.request.POST}') 
        logger.error(f'Failed to create forum: {form.errors}')
        return super().form_invalid(form)

class UpdateForumView(UpdateView):
    model = Forum
    form_class = ForumForm
    template_name = 'forum-update.html'
    context_object_name = 'post'

    def form_valid(self, form):
       
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('forum-list')