
from django.urls import path
from .views import ColorizationView
from . import views
from .views import (
   feedback_list,
    feedback_create,
    feedback_detail,
    feedback_update,
    feedback_delete,

    
)

urlpatterns = [
    path('colorize/', ColorizationView.as_view(), name='colorize'),


    # URL pour les feedbacks
    path('feedbacks/<int:feedback_id>/', views.feedback_detail, name='feedback_detail'),
    path('feedbacks/<int:feedback_id>/update/', views.feedback_update, name='feedback_update'),
    path('feedbacks/<int:feedback_id>/delete/', views.feedback_delete, name='feedback_delete'),
    path('feedbacks/', views.feedback_list, name='feedback_list'),  # Assurez-vous que le nom de la vue est correct

    path('feedbacks/create/', feedback_create, name='feedback_create'),  # Assurez-vous que ce chemin est correct

]


