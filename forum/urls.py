# forum/urls.py

from django.urls import path
from .views import ForumListView,CreateForumView 

urlpatterns = [
    path('', ForumListView.as_view(), name='forum-list'), 
    path('create/', CreateForumView.as_view(), name='create-forum'), 
]
