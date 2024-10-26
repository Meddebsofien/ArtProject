from django.urls import path
from . import views

urlpatterns = [
    path('', views.publication, name='publication_list'),  # Afficher toutes les publications
    path('create/', views.publication_create, name='publication_create'),  
    path('update/<str:pk>', views.publication_update, name='publication_update'), 
    path('details/<str:pk>', views.publication_details, name='publication_details'), 
    path('delete/<str:pk>', views.publication_delete, name='publication_delete'), 
    path('comment/<str:pk>', views.publication_comment, name='publication_comment'), 
    path('commentaire/delete/<str:pk>/', views.commentaire_delete, name='commentaire_delete'),




]
