from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_reclamations, name='liste_reclamations'),
    path('creer/', views.creer_reclamation, name='creer_reclamation'),
    path('<int:pk>/modifier/', views.modifier_reclamation, name='modifier_reclamation'),
    path('<int:pk>/supprimer/', views.supprimer_reclamation, name='supprimer_reclamation'),
]
