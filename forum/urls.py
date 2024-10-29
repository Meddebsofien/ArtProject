# forum/urls.py

from django.urls import path
from .views import ForumListView,CreateForumView , UpdateForumView, DeleteForumView

urlpatterns = [
    path('', ForumListView.as_view(), name='forum-list'), 
    path('create/', CreateForumView.as_view(), name='create-forum'), 
    path('update/<int:pk>/', UpdateForumView.as_view(), name='forum-update'),
    path('delete/<int:pk>/', DeleteForumView.as_view(), name='forum-delete'),
]
