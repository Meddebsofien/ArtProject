from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('reclamationsAdmin/', views.liste_reclamations, name='liste_reclamationsadmin'),
    path('repondre_reclamation/<int:reclamation_id>/', views.repondre_reclamation, name='repondre_reclamation'),

]
