
from django.urls import path
from .views import ColorizationView
from . import views
from .views import (
    reclamation_list,
    reclamation_create,
    reclamation_detail,
    reclamation_update,
    reclamation_delete,
    feedback_list,
    feedback_create,
    feedback_detail,
    feedback_update,
    feedback_delete,

    
)

urlpatterns = [
    path('colorize/', ColorizationView.as_view(), name='colorize'),

    path('reclamations/', views.reclamation_list, name='reclamation_list'),
    path('reclamations/create/', views.reclamation_create, name='reclamation_create'),
    path('reclamations/<int:reclamation_id>/', views.reclamation_detail, name='reclamation_detail'),
    path('reclamations/<int:reclamation_id>/update/', views.reclamation_update, name='reclamation_update'),
    path('reclamations/<int:reclamation_id>/delete/', views.reclamation_delete, name='reclamation_delete'),
    # URL pour les feedbacks
    path('feedbacks/<int:feedback_id>/', views.feedback_detail, name='feedback_detail'),
    path('feedbacks/<int:feedback_id>/update/', views.feedback_update, name='feedback_update'),
    path('feedbacks/<int:feedback_id>/delete/', views.feedback_delete, name='feedback_delete'),
    path('feedbacks/', views.feedback_list, name='feedback_list'),  # Assurez-vous que le nom de la vue est correct

    path('feedbacks/create/', feedback_create, name='feedback_create'),  # Assurez-vous que ce chemin est correct

]


